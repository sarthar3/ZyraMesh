import datetime
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, Text
from app.database import Base

class AgentModel(Base):
    __tablename__ = "agents"

    agent_id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, default="general")
    capabilities = Column(JSON, nullable=False, default=list)            # List[str]
    tools = Column(JSON, nullable=False, default=list)                   # List[Dict]
    model_backend = Column(String(100), nullable=False)                  # e.g. "ollama", "gemini", "mock"
    model_name = Column(String(100), nullable=False, default="qwen2.5:1.5b-instruct")
    input_schema = Column(JSON, nullable=False, default=dict)
    output_schema = Column(JSON, nullable=False, default=dict)
    cost_per_execution = Column(Float, nullable=False, default=0.001)
    cost_per_1k_tokens = Column(Float, nullable=False, default=0.001)
    expected_latency = Column(Integer, nullable=False, default=150)
    avg_latency_ms = Column(Integer, nullable=False, default=150)
    availability = Column(String(20), nullable=False, default="AVAILABLE") # AVAILABLE, BUSY, DEGRADED, UNAVAILABLE
    availability_status = Column(String(20), nullable=False, default="AVAILABLE")
    permissions = Column(JSON, nullable=False, default=list)             # List[str] security scopes
    provenance = Column(JSON, nullable=False, default=dict)              # Registration meta
    status = Column(String(20), nullable=False, default="ACTIVE")        # ACTIVE, INACTIVE, DEGRADED, UNAVAILABLE, SUSPENDED

    # Trust Metrics
    global_trust = Column(Float, nullable=False, default=0.5)
    trust_mean = Column(Float, nullable=False, default=0.5)
    trust_uncertainty = Column(Float, nullable=False, default=0.5)
    capability_specific_trust = Column(JSON, nullable=False, default=dict)# Dict[cap, {mean, var}]
    successful_executions = Column(Integer, nullable=False, default=0)
    failed_executions = Column(Integer, nullable=False, default=0)
    verifier_agreement = Column(Float, nullable=False, default=0.90)
    schema_validity = Column(Float, nullable=False, default=0.95)
    tool_success = Column(Float, nullable=False, default=0.95)
    recent_performance = Column(Float, nullable=False, default=0.85)
    historical_performance = Column(Float, nullable=False, default=0.85)
    collaboration_history = Column(JSON, nullable=False, default=dict)    # Dict[other_agent_id, {count, success_rate}]

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
