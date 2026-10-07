import datetime
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, ForeignKey
from app.database import Base

class AuditEventModel(Base):
    __tablename__ = "audit_events"

    event_id = Column(String(64), primary_key=True, index=True)
    workflow_id = Column(String(64), ForeignKey("workflows.workflow_id"), nullable=True)
    execution_id = Column(String(64), nullable=True)
    event_type = Column(String(50), nullable=False) # GUARDRAIL_CHECK, TDG_BUILT, ACTG_MATCHED, TEAM_FORMED, UNCERTAINTY_GATE_TRIGGERED, RE_ORCHESTRATED, TRUST_UPDATED
    actor = Column(String(100), nullable=False)
    payload = Column(JSON, nullable=False, default=dict)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class BenchmarkMetricModel(Base):
    __tablename__ = "benchmark_metrics"

    metric_id = Column(String(64), primary_key=True, index=True)
    run_id = Column(String(64), nullable=False)
    strategy = Column(String(50), nullable=False)
    ablation = Column(String(50), nullable=False, default="NONE")
    workflow_success_rate = Column(Float, nullable=False)
    failure_propagation_rate = Column(Float, nullable=False)
    expected_calibration_error = Column(Float, nullable=False)
    avg_latency_ms = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    verification_frequency = Column(Float, nullable=False)
    rerouting_success_rate = Column(Float, nullable=False)
    policy_violations_count = Column(Integer, nullable=False)
    sample_size = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
