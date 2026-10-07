import datetime
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, Text, ForeignKey
from app.database import Base

class WorkflowModel(Base):
    __tablename__ = "workflows"

    workflow_id = Column(String(64), primary_key=True, index=True)
    raw_user_objective = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="SUBMITTED") # SUBMITTED, ANALYZED, TEAM_FORMED, EXECUTING, COMPLETED, FAILED
    execution_strategy = Column(String(50), nullable=False, default="ZYRAMESH") # SINGLE_GENERALIST, FIXED_MULTI_AGENT, CAPABILITY_ONLY, REPUTATION_ONLY, DYNAMIC_BASELINE, ZYRAMESH
    ablation_config = Column(JSON, nullable=False, default=dict)
    max_budget = Column(Float, nullable=True)
    max_latency_ms = Column(Integer, nullable=True)
    required_security_tier = Column(String(50), nullable=True)
    tdg_structure = Column(JSON, nullable=True)                      # Nodes and edges of TDG
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(String(64), primary_key=True, index=True)
    workflow_id = Column(String(64), ForeignKey("workflows.workflow_id", ondelete="CASCADE"), nullable=False)
    subtask_index = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    required_capabilities = Column(JSON, nullable=False, default=list)
    required_tools = Column(JSON, nullable=False, default=list)
    input_schema = Column(JSON, nullable=False, default=dict)
    output_schema = Column(JSON, nullable=False, default=dict)
    sensitivity_score = Column(Float, nullable=False, default=0.0)
    criticality_score = Column(Float, nullable=False, default=0.5)
    propagation_risk = Column(Float, nullable=False, default=0.5)
    verification_requirement = Column(String(30), nullable=False, default="AUTO")
    dependencies = Column(JSON, nullable=False, default=list)        # list of parent task_ids
    assigned_agent_id = Column(String(64), ForeignKey("agents.agent_id"), nullable=True)
    status = Column(String(30), nullable=False, default="PENDING")
