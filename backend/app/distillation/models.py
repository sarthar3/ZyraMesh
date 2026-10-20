import datetime
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, Text, ForeignKey
from app.database import Base

class DistillationJobModel(Base):
    """
    Tracks Distillation-as-a-Service (DaaS) training jobs.
    Distills heavy multi-agent orchestration or frontier LLMs into compact edge models.
    """
    __tablename__ = "distillation_jobs"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
    
    # Teacher & Student Specs
    teacher_model = Column(String(100), nullable=False, default="zyra-mesh-orchestrator")
    student_base = Column(String(100), nullable=False, default="qwen2.5:0.5b")
    distillation_strategy = Column(String(50), nullable=False, default="SEQUENCE_KD")  # SEQUENCE_KD, MULTI_AGENT_TRAJECTORY, COT_REASONING, LOGIT_KL
    
    # Dataset & Training Config
    dataset_id = Column(String(64), nullable=True)
    dataset_name = Column(String(255), nullable=True)
    dataset_size = Column(Integer, nullable=False, default=100)
    epochs = Column(Integer, nullable=False, default=3)
    batch_size = Column(Integer, nullable=False, default=4)
    learning_rate = Column(Float, nullable=False, default=2e-5)
    temperature = Column(Float, nullable=False, default=2.0)
    alpha_kd = Column(Float, nullable=False, default=0.7)  # Weight of KD loss vs task loss
    
    # Live Progress Tracking
    current_epoch = Column(Integer, nullable=False, default=0)
    current_step = Column(Integer, nullable=False, default=0)
    total_steps = Column(Integer, nullable=False, default=100)
    progress_percentage = Column(Float, nullable=False, default=0.0)
    loss_history = Column(JSON, nullable=False, default=list)  # List of {epoch, step, total_loss, ce_loss, kl_loss, perplexity}
    
    # Performance & ROI Metrics
    teacher_latency_ms = Column(Integer, nullable=False, default=4200)
    student_latency_ms = Column(Integer, nullable=False, default=65)
    latency_reduction_pct = Column(Float, nullable=False, default=98.4)
    teacher_cost_per_1k = Column(Float, nullable=False, default=0.015)
    student_cost_per_1k = Column(Float, nullable=False, default=0.0001)
    cost_reduction_pct = Column(Float, nullable=False, default=99.3)
    compression_ratio = Column(String(20), nullable=False, default="18.5x")
    accuracy_retention_pct = Column(Float, nullable=False, default=95.8)
    
    # Output Model Artifacts
    export_format = Column(String(30), nullable=False, default="GGUF_Q4_K_M")  # GGUF_Q4_K_M, GGUF_Q8_0, ONNX, SAFETENSORS
    export_path = Column(String(500), nullable=True)
    ollama_modelfile = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class DistillationDatasetModel(Base):
    """
    Stores curated or synthesized datasets used for knowledge distillation.
    Filtered through Zyra's Uncertainty Gate to ensure only high-trust traces are distilled.
    """
    __tablename__ = "distillation_datasets"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(100), nullable=False, default="general")
    source = Column(String(50), nullable=False, default="ZYRA_VERIFIED_WORKFLOWS")  # ZYRA_VERIFIED_WORKFLOWS, SYNTHETIC_TEACHER, CUSTOM_UPLOAD
    
    num_samples = Column(Integer, nullable=False, default=0)
    samples = Column(JSON, nullable=False, default=list)  # List of {id, prompt, teacher_output, rationale, confidence, verified}
    avg_trust_score = Column(Float, nullable=False, default=0.92)
    avg_uncertainty = Column(Float, nullable=False, default=0.18)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class DistilledModelRegistryModel(Base):
    """
    Catalog of deploy-ready distilled student models.
    Can be loaded directly for real-time inference or exported to Ollama/GGUF/Edge.
    """
    __tablename__ = "distilled_models"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    base_architecture = Column(String(100), nullable=False)  # e.g., "Qwen2.5-0.5B-Instruct"
    teacher_lineage = Column(String(100), nullable=False)    # e.g., "Zyra Mesh 7-Agent Ensemble"
    job_id = Column(String(64), nullable=True)
    
    parameters = Column(String(20), nullable=False, default="490M")
    quantization = Column(String(20), nullable=False, default="Q4_K_M")
    model_size_mb = Column(Float, nullable=False, default=380.0)
    
    avg_latency_ms = Column(Integer, nullable=False, default=55)
    accuracy_retention = Column(Float, nullable=False, default=96.2)
    ram_usage_mb = Column(Integer, nullable=False, default=420)
    status = Column(String(20), nullable=False, default="READY")  # READY, DEPLOYED, BENCHMARKING
    
    ollama_model_name = Column(String(100), nullable=True)
    download_url = Column(String(255), nullable=True)
    api_endpoint = Column(String(255), nullable=True)
    
    sample_system_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
