from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.execution import ExecutionModel
from app.models.agent import AgentModel
from app.schemas.execution import ExecutionResponse

router = APIRouter(prefix="/executions", tags=["Executions & Audit Logs"])

@router.get("/workflow/{workflow_id}", response_model=List[ExecutionResponse])
def get_workflow_executions(workflow_id: str, db: Session = Depends(get_db)):
    execs = db.query(ExecutionModel).filter(ExecutionModel.workflow_id == workflow_id).all()
    agents = {a.agent_id: a.name for a in db.query(AgentModel).all()}

    results = []
    for e in execs:
        item = ExecutionResponse(
            execution_id=e.execution_id,
            workflow_id=e.workflow_id,
            task_id=e.task_id,
            agent_id=e.agent_id,
            agent_name=agents.get(e.agent_id, "Unknown"),
            input_data=e.input_data,
            output_data=e.output_data,
            confidence_score=e.confidence_score,
            uncertainty_score=e.uncertainty_score,
            schema_valid=e.schema_valid,
            verifier_agreement=e.verifier_agreement,
            evidence_score=e.evidence_score,
            tool_trace=e.tool_trace or [],
            policy_status=e.policy_status,
            start_time=e.start_time,
            end_time=e.end_time,
            status=e.status
        )
        results.append(item)
    return results
