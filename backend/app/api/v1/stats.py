from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from app.database import get_db
from app.models.agent import AgentModel
from app.models.task import WorkflowModel
from app.models.execution import ExecutionModel
from app.models.trust import TrustObservationModel
from app.models.audit import AuditEventModel

router = APIRouter(prefix="/stats", tags=["Home Overview Metrics"])

@router.get("/overview")
def get_system_overview_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    total_agents = db.query(AgentModel).count()
    active_agents = db.query(AgentModel).filter(AgentModel.status == "ACTIVE").count()

    total_workflows = db.query(WorkflowModel).count()
    succ_workflows = db.query(WorkflowModel).filter(WorkflowModel.status == "COMPLETED").count()
    running_workflows = db.query(WorkflowModel).filter(WorkflowModel.status.in_(["RUNNING", "PLANNING", "TEAM_FORMED"])).count()

    re_orchestrations = db.query(AuditEventModel).filter(AuditEventModel.event_type == "RE_ORCHESTRATED").count()

    agents = db.query(AgentModel).all()
    avg_trust = round(sum(a.trust_mean for a in agents) / max(1, len(agents)), 4) if agents else 0.5

    executions = db.query(ExecutionModel).all()
    avg_latency = round(sum(e.latency_ms or 0 for e in executions) / max(1, len(executions)), 1) if executions else 350.0
    est_cost = round(sum(e.cost or 0.0 for e in executions), 5) if executions else 0.0425

    verified_execs = db.query(ExecutionModel).filter(ExecutionModel.verifier_agreement > 0.0).count()
    verif_rate = round(verified_execs / max(1, len(executions)), 3) if executions else 0.333

    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "total_workflows": total_workflows,
        "successful_workflows": succ_workflows,
        "current_running_workflows": running_workflows,
        "re_orchestrations": re_orchestrations,
        "average_trust": avg_trust,
        "average_latency_ms": avg_latency,
        "estimated_cost_usd": est_cost,
        "verification_rate": verif_rate
    }
