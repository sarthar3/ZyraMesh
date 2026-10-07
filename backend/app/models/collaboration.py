import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from app.database import Base

class CollaborationMemoryModel(Base):
    __tablename__ = "collaboration_memory"

    pair_id = Column(String(128), primary_key=True, index=True) # e.g. "agent_a->agent_b"
    source_agent_id = Column(String(64), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    target_agent_id = Column(String(64), ForeignKey("agents.agent_id", ondelete="CASCADE"), nullable=False)
    successful_handoffs = Column(Integer, nullable=False, default=0)
    failed_handoffs = Column(Integer, nullable=False, default=0)
    schema_compatibility_rate = Column(Float, nullable=False, default=1.0)
    verifier_agreement_rate = Column(Float, nullable=False, default=1.0)
    average_handoff_latency_ms = Column(Float, nullable=False, default=0.0)
    compatibility_score = Column(Float, nullable=False, default=0.90)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
