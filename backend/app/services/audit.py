import uuid
import datetime
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.models.audit import AuditEventModel
from app.models.task import WorkflowModel, TaskModel
from app.models.execution import ExecutionModel
from app.models.trust import TrustObservationModel

class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        event_type: str,
        actor: str,
        payload: Dict[str, Any],
        workflow_id: Optional[str] = None,
        execution_id: Optional[str] = None
    ) -> AuditEventModel:
        event = AuditEventModel(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            workflow_id=workflow_id,
            execution_id=execution_id,
            event_type=event_type,
            actor=actor,
            payload=payload,
            timestamp=datetime.datetime.utcnow()
        )
        db.add(event)
        try:
            db.commit()
            db.refresh(event)
        except Exception:
            db.rollback()
        return event

    @staticmethod
    def get_workflow_audit_trace(db: Session, workflow_id: str) -> Dict[str, Any]:
        wf = db.query(WorkflowModel).filter(WorkflowModel.workflow_id == workflow_id).first()
        if not wf:
            return {"error": f"Workflow {workflow_id} not found"}

        tasks = db.query(TaskModel).filter(TaskModel.workflow_id == workflow_id).order_by(TaskModel.subtask_index).all()
        executions = db.query(ExecutionModel).filter(ExecutionModel.workflow_id == workflow_id).order_by(ExecutionModel.start_time).all()
        events = db.query(AuditEventModel).filter(AuditEventModel.workflow_id == workflow_id).order_by(AuditEventModel.timestamp).all()
        trust_obs = db.query(TrustObservationModel).filter(TrustObservationModel.workflow_id == workflow_id).order_by(TrustObservationModel.timestamp).all()

        total_cost = sum(e.cost or 0.0 for e in executions)
        total_latency = sum(e.latency_ms or 0 for e in executions)

        return {
            "workflow_id": wf.workflow_id,
            "raw_user_objective": wf.raw_user_objective,
            "status": wf.status,
            "execution_strategy": wf.execution_strategy,
            "ablation_config": wf.ablation_config or {},
            "created_at": wf.created_at.isoformat() if wf.created_at else None,
            "completed_at": wf.completed_at.isoformat() if wf.completed_at else None,
            "summary": {
                "total_tasks": len(tasks),
                "total_executions": len(executions),
                "total_events": len(events),
                "total_trust_updates": len(trust_obs),
                "total_cost": round(total_cost, 6),
                "total_latency_ms": total_latency
            },
            "tdg_structure": wf.tdg_structure,
            "tasks": [
                {
                    "task_id": t.task_id,
                    "subtask_index": t.subtask_index,
                    "description": t.description,
                    "required_capabilities": t.required_capabilities,
                    "assigned_agent_id": t.assigned_agent_id,
                    "status": t.status
                } for t in tasks
            ],
            "executions": [
                {
                    "execution_id": e.execution_id,
                    "task_id": e.task_id,
                    "agent_id": e.agent_id,
                    "input_data": e.input_data,
                    "output_data": e.output_data,
                    "confidence_score": e.confidence_score,
                    "uncertainty_score": e.uncertainty_score,
                    "status": e.status,
                    "latency_ms": e.latency_ms,
                    "cost": e.cost,
                    "tool_trace": e.tool_trace or [],
                    "start_time": e.start_time.isoformat() if e.start_time else None,
                    "end_time": e.end_time.isoformat() if e.end_time else None
                } for e in executions
            ],
            "events": [
                {
                    "event_id": ev.event_id,
                    "event_type": ev.event_type,
                    "actor": ev.actor,
                    "payload": ev.payload,
                    "timestamp": ev.timestamp.isoformat() if ev.timestamp else None
                } for ev in events
            ],
            "trust_updates": [
                {
                    "observation_id": tr.observation_id,
                    "agent_id": tr.agent_id,
                    "capability": tr.capability,
                    "old_trust": tr.old_trust,
                    "new_trust": tr.new_trust,
                    "success": tr.success,
                    "timestamp": tr.timestamp.isoformat() if tr.timestamp else None
                } for tr in trust_obs
            ]
        }
