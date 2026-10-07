import datetime
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, Text, Boolean, ForeignKey
from app.database import Base

class ExecutionModel(Base):
    __tablename__ = "executions"

    execution_id = Column(String(64), primary_key=True, index=True)
    workflow_id = Column(String(64), ForeignKey("workflows.workflow_id", ondelete="CASCADE"), nullable=False)
    task_id = Column(String(64), ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=False)
    agent_id = Column(String(64), ForeignKey("agents.agent_id"), nullable=False)
    input_data = Column(JSON, nullable=False, default=dict)
    output_data = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    uncertainty_score = Column(Float, nullable=True)
    schema_valid = Column(Boolean, nullable=True)
    verifier_agreement = Column(Float, nullable=True)
    evidence_score = Column(Float, nullable=True)
    tool_trace = Column(JSON, nullable=False, default=list)
    policy_status = Column(String(30), nullable=False, default="PASSED") # PASSED, VIOLATION_BLOCKED, WARNED
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(30), nullable=False, default="RUNNING") # RUNNING, SUCCESS, FAILED, VERIFYING, RE_ROUTED
