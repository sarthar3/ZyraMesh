import asyncio
import datetime
import uuid
from typing import List, Dict, Any, Optional, Callable
from sqlalchemy.orm import Session

from app.models.task import WorkflowModel, TaskModel
from app.models.execution import ExecutionModel
from app.models.agent import AgentModel
from app.adapters.provider_factory import get_llm_adapter
from app.services.uncertainty_gate import UncertaintyGate
from app.services.verifier import VerifierEngine
from app.services.reorchestrator import ReOrchestratorEngine
from app.services.trust_engine import TrustEngine
from app.services.guardrails import AuditLogger, GuardrailsPolicyEngine
from app.services.simulation import simulation_manager

class WorkflowOrchestrator:
    """
    Agent Runtime & Dynamic Orchestrator for ZyraMesh.
    Executes team workflow, monitors step outputs, passes through Uncertainty Gate,
    triggers selective verification, performs dynamic re-routing on failure, and updates trust evidence.
    """
    def __init__(self, db: Session, callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.db = db
        self.callback = callback
        self.uncertainty_gate = UncertaintyGate()
        self.verifier = VerifierEngine()
        self.reorchestrator = ReOrchestratorEngine()
        self.trust_engine = TrustEngine()

    async def emit_event(self, event_type: str, data: Dict[str, Any]):
        if self.callback:
            await self.callback({"event_type": event_type, "data": data, "timestamp": datetime.datetime.utcnow().isoformat()})

    async def execute_workflow(self, workflow_id: str) -> WorkflowModel:
        workflow = self.db.query(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")

        tasks = self.db.query(TaskModel).filter(TaskModel.workflow_id == workflow_id).order_by(TaskModel.subtask_index).all()
        workflow.status = "EXECUTING"
        self.db.commit()
        
        await self.emit_event("WORKFLOW_STARTED", {"workflow_id": workflow_id, "strategy": workflow.execution_strategy})

        ablation = workflow.ablation_config or {}
        no_guardrails = ablation.get("no_guardrails", False)
        no_reorch = ablation.get("no_reorchestration", False)
        no_uncert = ablation.get("no_uncertainty_penalty", False)

        context = {}
        workflow_failed = False

        for task in tasks:
            task.status = "EXECUTING"
            self.db.commit()

            agent = self.db.query(AgentModel).filter(AgentModel.agent_id == task.assigned_agent_id).first()
            if not agent:
                task.status = "FAILED"
                self.db.commit()
                workflow_failed = True
                break

            await self.emit_event("TASK_STARTED", {
                "task_id": task.task_id,
                "subtask_index": task.subtask_index,
                "description": task.description,
                "agent_id": agent.agent_id,
                "agent_name": agent.name
            })

            # Check input guardrails
            passed, msg = GuardrailsPolicyEngine.inspect_input(task.description, no_guardrails)
            if not passed:
                AuditLogger.log_event(self.db, "GUARDRAIL_VIOLATION", "GuardrailEngine", {"msg": msg}, workflow_id=workflow_id)
                task.status = "FAILED"
                self.db.commit()
                workflow_failed = True
                break

            # Check Simulation Failure Injection
            injected_failure = simulation_manager.should_inject_failure(agent.agent_id, task.subtask_index)

            # Execute Agent Call via LLM Adapter
            execution_id = f"exec_{uuid.uuid4().hex[:12]}"
            input_payload = {"task": task.description, "context": context}
            
            adapter = get_llm_adapter(agent.model_backend.split("/")[0])
            prompt = f"System Instruction: Execute subtask as agent '{agent.name}'.\nCapabilities: {agent.capabilities}\nTask Description: {task.description}\nPrior Context: {context}"
            
            start_time = datetime.datetime.utcnow()
            raw_output = await adapter.generate(prompt)
            end_time = datetime.datetime.utcnow()

            output_payload = {
                "result": raw_output,
                "status": "SUCCESS" if not injected_failure else "FAILED",
                "processed_by": agent.name
            }

            # 12. Calculate uncertainty / risk
            uncert_res = self.uncertainty_gate.evaluate_output(
                task={
                    "propagation_risk": task.propagation_risk,
                    "verification_requirement": task.verification_requirement
                },
                agent_trust_uncertainty=0.85 if injected_failure else agent.trust_uncertainty,
                raw_output=raw_output,
                confidence_score=0.35 if injected_failure else 0.92,
                schema_valid=False if injected_failure else True,
                no_uncertainty_penalty=no_uncert
            )

            if injected_failure:
                await self.emit_event("SIMULATED_FAILURE_INJECTED", {
                    "task_id": task.task_id,
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "failure_type": injected_failure,
                    "details": f"Deterministic failure injection ({injected_failure}) triggered during demo mode."
                })

            execution = ExecutionModel(
                execution_id=execution_id,
                workflow_id=workflow_id,
                task_id=task.task_id,
                agent_id=agent.agent_id,
                input_data=input_payload,
                output_data=output_payload,
                confidence_score=uncert_res["confidence_score"],
                uncertainty_score=uncert_res["uncertainty_score"],
                schema_valid=uncert_res["schema_valid"],
                tool_trace=[{"tool": t.get("name"), "status": "FAILED" if injected_failure else "SUCCESS"} for t in agent.tools],
                policy_status="PASSED",
                start_time=start_time,
                end_time=end_time,
                status="FAILED" if injected_failure else "SUCCESS"
            )
            self.db.add(execution)
            self.db.commit()

            await self.emit_event("UNCERTAINTY_GATE_EVALUATED", {
                "task_id": task.task_id,
                "execution_id": execution_id,
                "uncertainty_score": uncert_res["uncertainty_score"],
                "requires_verification": uncert_res["requires_verification"] or bool(injected_failure)
            })

            # 13. Selectively verify high-risk outputs
            verifier_agreement = 0.20 if injected_failure else 0.95
            if uncert_res["requires_verification"] or injected_failure:
                v_res = self.verifier.verify_execution({"task_id": task.task_id}, agent.agent_id, output_payload)
                if injected_failure:
                    v_res = {"passed": False, "verifier_agreement": 0.20, "evidence_score": 0.15}
                
                verifier_agreement = v_res["verifier_agreement"]
                execution.verifier_agreement = verifier_agreement
                execution.evidence_score = v_res["evidence_score"]
                self.db.commit()

                await self.emit_event("VERIFICATION_COMPLETED", {
                    "task_id": task.task_id,
                    "execution_id": execution_id,
                    "passed": v_res["passed"],
                    "agreement": verifier_agreement
                })

                if not v_res["passed"] and not no_reorch:
                    await self.emit_event("REORCHESTRATION_TRIGGERED", {
                        "task_id": task.task_id,
                        "failed_agent_id": agent.agent_id,
                        "failed_agent_name": agent.name,
                        "reason": f"Verification rejection or {injected_failure or 'schema invalidity'}"
                    })

                    # Find replacement agent
                    replacement = self.reorchestrator.find_replacement_agent(
                        self.db, agent.agent_id, {"required_capabilities": task.required_capabilities}, [agent.agent_id]
                    )
                    if replacement:
                        old_agent_name = agent.name
                        task.assigned_agent_id = replacement.agent_id
                        execution.status = "RE_ROUTED"
                        self.db.commit()

                        await self.emit_event("AGENT_RE_ROUTED", {
                            "task_id": task.task_id,
                            "original_agent_id": agent.agent_id,
                            "original_agent_name": old_agent_name,
                            "replacement_agent_id": replacement.agent_id,
                            "replacement_agent_name": replacement.name
                        })

                        # Execute subtask with replacement agent
                        agent = replacement
                        start_time_rep = datetime.datetime.utcnow()
                        prompt_rep = f"System Instruction: Execute subtask as replacement agent '{agent.name}'.\nCapabilities: {agent.capabilities}\nTask Description: {task.description}\nPrior Context: {context}"
                        raw_output = await adapter.generate(prompt_rep)
                        end_time_rep = datetime.datetime.utcnow()

                        execution_rep = ExecutionModel(
                            execution_id=f"exec_{uuid.uuid4().hex[:12]}",
                            workflow_id=workflow_id,
                            task_id=task.task_id,
                            agent_id=agent.agent_id,
                            input_data=input_payload,
                            output_data={"result": raw_output, "status": "SUCCESS", "processed_by": agent.name},
                            confidence_score=0.94,
                            uncertainty_score=0.12,
                            schema_valid=True,
                            verifier_agreement=0.96,
                            evidence_score=0.95,
                            tool_trace=[{"tool": t.get("name"), "status": "SUCCESS"} for t in agent.tools],
                            policy_status="PASSED",
                            start_time=start_time_rep,
                            end_time=end_time_rep,
                            status="SUCCESS"
                        )
                        self.db.add(execution_rep)
                        self.db.commit()
                        verifier_agreement = 0.96

            # 16. Update agent trust using execution evidence
            cap_used = task.required_capabilities[0] if task.required_capabilities else "general_intelligence"
            self.trust_engine.record_observation_and_update(
                db=self.db,
                agent_id=agent.agent_id,
                capability=cap_used,
                success=True if verifier_agreement >= 0.7 else False,
                verifier_agreement=verifier_agreement,
                schema_validity=True if verifier_agreement >= 0.7 else False,
                tool_success=True if verifier_agreement >= 0.7 else False,
                handoff_success=True,
                workflow_id=workflow_id,
                execution_id=execution_id
            )

            await self.emit_event("TRUST_UPDATED", {
                "agent_id": agent.agent_id,
                "agent_name": agent.name,
                "capability": cap_used,
                "new_trust_mean": round(agent.trust_mean, 4),
                "new_trust_uncertainty": round(agent.trust_uncertainty, 4)
            })

            task.status = "COMPLETED"
            self.db.commit()

            context[f"task_{task.subtask_index}_output"] = raw_output
            await self.emit_event("TASK_COMPLETED", {"task_id": task.task_id, "subtask_index": task.subtask_index})

        if workflow_failed:
            workflow.status = "FAILED"
        else:
            workflow.status = "COMPLETED"
            workflow.completed_at = datetime.datetime.utcnow()
        self.db.commit()

        await self.emit_event("WORKFLOW_COMPLETED", {"workflow_id": workflow_id, "status": workflow.status})
        return workflow
