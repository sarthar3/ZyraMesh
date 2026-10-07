import asyncio
import datetime
import uuid
import json
from typing import List, Dict, Any, Optional, Callable
from sqlalchemy.orm import Session

from app.models.task import WorkflowModel, TaskModel
from app.models.execution import ExecutionModel
from app.models.agent import AgentModel
from app.agents.local_llm_agent import LocalLLMAgent
from app.agents.mock_agent import MockAgent
from app.verification.uncertainty_gate import UncertaintyGate
from app.verification.verifier import VerificationAgent
from app.orchestration.reorchestrator import ReOrchestratorEngine
from app.trust.trust_engine import TrustEngine
from app.guardrails.policy_engine import GuardrailsPolicyEngine
from app.services.guardrails import AuditLogger
from app.core.logging import logger

class WorkflowOrchestrator:
    """
    Module 9: Runtime Orchestrator for ZyraMesh.
    Manages workflow lifecycle across states:
      CREATED -> PLANNING -> TEAM_FORMED -> RUNNING -> WAITING -> VERIFYING -> RETRYING -> REORCHESTRATING -> COMPLETED / FAILED / HUMAN_REVIEW.
    Concurrently resolves dependencies, invokes universal Agent Execution Protocol, evaluates Uncertainty Gate,
    triggers Selective Verification & Dynamic Re-Orchestration, and emits WebSocket event stream.
    """
    def __init__(self, db: Session, callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.db = db
        self.callback = callback
        self.uncertainty_gate = UncertaintyGate()
        self.verifier = VerificationAgent()
        self.reorchestrator = ReOrchestratorEngine()
        self.trust_engine = TrustEngine()

    async def emit_event(self, event_type: str, data: Dict[str, Any]):
        event_payload = {
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        logger.info(f"Orchestrator Event [{event_type}]: {data}")
        if self.callback:
            try:
                await self.callback(event_payload)
            except Exception:
                pass

    async def execute_workflow(self, workflow_id: str) -> WorkflowModel:
        workflow = self.db.query(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow '{workflow_id}' not found.")

        tasks = self.db.query(TaskModel).filter(TaskModel.workflow_id == workflow_id).order_by(TaskModel.subtask_index).all()
        workflow.status = "RUNNING"
        self.db.commit()

        await self.emit_event("WORKFLOW_STARTED", {
            "workflow_id": workflow_id,
            "strategy": workflow.execution_strategy,
            "total_tasks": len(tasks)
        })

        ablation = workflow.ablation_config or {}
        no_guardrails = ablation.get("no_guardrails", False)
        no_reorch = ablation.get("no_reorchestration", False)
        no_uncert = ablation.get("no_uncertainty_penalty", False)

        context = {}
        excluded_agent_ids = []

        for task in tasks:
            task.status = "RUNNING"
            self.db.commit()

            agent_model = self.db.query(AgentModel).filter(AgentModel.agent_id == task.assigned_agent_id).first()
            if not agent_model:
                task.status = "FAILED"
                workflow.status = "FAILED"
                self.db.commit()
                break

            await self.emit_event("TASK_STARTED", {
                "task_id": task.task_id,
                "subtask_index": task.subtask_index,
                "description": task.description,
                "agent_id": agent_model.agent_id,
                "agent_name": agent_model.name
            })

            # 1. Guardrail Input Check
            passed, policy_msg = GuardrailsPolicyEngine.inspect_input(task.description, no_guardrails)
            if not passed:
                AuditLogger.log_event(self.db, "GUARDRAIL_VIOLATION", "GuardrailPolicyEngine", {"msg": policy_msg}, workflow_id=workflow_id)
                task.status = "FAILED"
                workflow.status = "FAILED"
                self.db.commit()
                await self.emit_event("TASK_FAILED", {"task_id": task.task_id, "reason": policy_msg})
                break

            # 2. Universal Agent Execution
            if agent_model.model_backend == "mock":
                agent_instance = MockAgent(agent_model.agent_id, agent_model.name)
            else:
                agent_instance = LocalLLMAgent(agent_model.agent_id, agent_model.name, model_name=agent_model.model_name)

            execution_id = f"exec_{uuid.uuid4().hex[:12]}"
            start_time = datetime.datetime.utcnow()

            task_payload = {
                "task_id": task.task_id,
                "subtask_index": task.subtask_index,
                "description": task.description,
                "propagation_risk": task.propagation_risk,
                "criticality": task.criticality,
                "verification_required": task.verification_requirement
            }

            agent_res = await agent_instance.execute(task_payload, context)
            end_time = datetime.datetime.utcnow()

            # 3. Uncertainty Gate Evaluation
            uncert_res = self.uncertainty_gate.evaluate(
                task=task_payload,
                agent_trust_uncertainty=agent_model.trust_uncertainty,
                confidence_score=agent_res.confidence,
                schema_valid=agent_res.schema_valid,
                no_uncertainty_penalty=no_uncert
            )

            await self.emit_event("UNCERTAINTY_EVALUATED", {
                "task_id": task.task_id,
                "uncertainty_score": uncert_res["uncertainty_score"],
                "risk_level": uncert_res["risk_level"],
                "recommended_action": uncert_res["recommended_action"]
            })

            # 4. Selective Verification System
            verifier_agreement = 0.95
            if uncert_res["requires_verification"]:
                workflow.status = "VERIFYING"
                self.db.commit()
                await self.emit_event("VERIFICATION_STARTED", {"task_id": task.task_id})

                v_res = self.verifier.verify(task_payload, agent_model.agent_id, agent_res.output, agent_res.schema_valid)
                verifier_agreement = v_res["verifier_agreement"]

                await self.emit_event("VERIFICATION_COMPLETED", {
                    "task_id": task.task_id,
                    "passed": v_res["passed"],
                    "agreement_score": verifier_agreement,
                    "action": v_res["recommended_action"]
                })

                # 5. Dynamic Re-Orchestration Trigger
                if not v_res["passed"] and not no_reorch:
                    workflow.status = "REORCHESTRATING"
                    self.db.commit()
                    await self.emit_event("REORCHESTRATION_STARTED", {"task_id": task.task_id, "failed_agent": agent_model.agent_id})

                    excluded_agent_ids.append(agent_model.agent_id)
                    replacement = self.reorchestrator.find_replacement_agent(
                        self.db, agent_model.agent_id, {"required_capabilities": task.required_capabilities}, excluded_agent_ids
                    )

                    if replacement:
                        task.assigned_agent_id = replacement.agent_id
                        self.db.commit()
                        await self.emit_event("AGENT_REPLACED", {
                            "task_id": task.task_id,
                            "original_agent_id": agent_model.agent_id,
                            "replacement_agent_id": replacement.agent_id
                        })
                        agent_model = replacement
                        # Re-execute with replacement
                        agent_instance = MockAgent(agent_model.agent_id, agent_model.name)
                        agent_res = await agent_instance.execute(task_payload, context)

            # Record Execution
            exec_record = ExecutionModel(
                execution_id=execution_id,
                workflow_id=workflow_id,
                task_id=task.task_id,
                agent_id=agent_model.agent_id,
                input_data=task_payload,
                output_data=agent_res.output if isinstance(agent_res.output, dict) else {"result": str(agent_res.output)},
                confidence_score=agent_res.confidence,
                uncertainty_score=uncert_res["uncertainty_score"],
                schema_valid=agent_res.schema_valid,
                verifier_agreement=verifier_agreement,
                evidence_score=0.95,
                tool_trace=agent_res.tool_trace,
                policy_status="PASSED",
                start_time=start_time,
                end_time=end_time,
                status="SUCCESS" if agent_res.success else "FAILED"
            )
            self.db.add(exec_record)

            # 6. Evidence-Driven Trust Update
            cap_used = task.required_capabilities[0] if task.required_capabilities else "general"
            self.trust_engine.record_observation_and_update(
                db=self.db,
                agent_id=agent_model.agent_id,
                capability=cap_used,
                success=agent_res.success,
                verifier_agreement=verifier_agreement,
                schema_validity=agent_res.schema_valid,
                tool_success=True,
                handoff_success=True,
                workflow_id=workflow_id,
                execution_id=execution_id
            )

            task.status = "COMPLETED"
            self.db.commit()

            context[f"task_{task.subtask_index}_output"] = agent_res.output
            await self.emit_event("TASK_COMPLETED", {"task_id": task.task_id, "subtask_index": task.subtask_index})

        workflow.status = "COMPLETED"
        workflow.completed_at = datetime.datetime.utcnow()
        self.db.commit()

        await self.emit_event("WORKFLOW_COMPLETED", {"workflow_id": workflow_id, "status": workflow.status})
        return workflow
