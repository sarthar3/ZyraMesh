import datetime
from sqlalchemy import Column, String, Float, JSON, DateTime, Boolean, ForeignKey
from app.database import Base

class TrustObservationModel(Base):
    __tablename__ = "trust_observations"

    observation_id = Column(String(64), primary_key=True, index=True)
    agent_id = Column(String(64), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    workflow_id = Column(String(64), ForeignKey("workflows.workflow_id"), nullable=True)
    execution_id = Column(String(64), ForeignKey("executions.execution_id"), nullable=True)
    capability = Column(String(100), nullable=False)
    success = Column(Boolean, nullable=False)
    verifier_agreement = Column(Float, nullable=True)
    schema_validity = Column(Boolean, nullable=False)
    tool_success = Column(Boolean, nullable=False)
    handoff_success = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    evidence_source = Column(String(100), nullable=False)
