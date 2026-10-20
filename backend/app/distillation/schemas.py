from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class DistillationJobCreate(BaseModel):
    name: str = Field(..., example="Zyra-Shopping-Fast-Distill-1B")
    description: Optional[str] = Field(None, example="Distilling 7-agent Zyra mesh shopping knowledge into Qwen2.5 0.5B")
    teacher_model: str = Field("zyra-mesh-orchestrator", example="zyra-mesh-orchestrator")
    student_base: str = Field("qwen2.5:0.5b", example="qwen2.5:0.5b")
    distillation_strategy: str = Field("SEQUENCE_KD", example="SEQUENCE_KD")
    dataset_id: Optional[str] = Field(None, example="dataset_shopping_verified_v1")
    epochs: int = Field(3, ge=1, le=20)
    batch_size: int = Field(4, ge=1, le=64)
    learning_rate: float = Field(2e-5, gt=0)
    temperature: float = Field(2.0, ge=1.0, le=5.0)
    alpha_kd: float = Field(0.7, ge=0.0, le=1.0)
    export_format: str = Field("GGUF_Q4_K_M", example="GGUF_Q4_K_M")

class LossPoint(BaseModel):
    epoch: int
    step: int
    total_loss: float
    ce_loss: float
    kl_loss: float
    perplexity: float
    tokens_per_sec: float

class DistillationJobResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    teacher_model: str
    student_base: str
    distillation_strategy: str
    dataset_size: int
    epochs: int
    current_epoch: int
    current_step: int
    total_steps: int
    progress_percentage: float
    latency_reduction_pct: float
    cost_reduction_pct: float
    compression_ratio: str
    accuracy_retention_pct: float
    teacher_latency_ms: int
    student_latency_ms: int
    export_format: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DistillationJobDetail(DistillationJobResponse):
    loss_history: List[Dict[str, Any]] = []
    ollama_modelfile: Optional[str] = None
    export_path: Optional[str] = None
    error_message: Optional[str] = None

class DatasetSample(BaseModel):
    id: str
    prompt: str
    teacher_output: str
    rationale: Optional[str] = None
    confidence: float = 0.95
    verified: bool = True

class DatasetGenerateRequest(BaseModel):
    name: str = Field(..., example="Ecommerce Specification Trajectories")
    domain: str = Field("shopping", example="shopping")
    num_samples: int = Field(20, ge=5, le=500)
    teacher_source: str = Field("zyra-mesh", example="zyra-mesh")  # zyra-mesh, gemini, ollama
    uncertainty_threshold: float = Field(0.35, ge=0.1, le=0.9)  # Filter samples with higher uncertainty

class DistillationDatasetResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    domain: str
    source: str
    num_samples: int
    avg_trust_score: float
    avg_uncertainty: float
    created_at: datetime

    class Config:
        from_attributes = True

class DistilledModelResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    base_architecture: str
    teacher_lineage: str
    parameters: str
    quantization: str
    model_size_mb: float
    avg_latency_ms: int
    accuracy_retention: float
    ram_usage_mb: int
    status: str
    ollama_model_name: Optional[str]
    download_url: Optional[str]
    api_endpoint: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DistillationInferenceRequest(BaseModel):
    prompt: str = Field(..., example="Find the best laptop under ₹70,000 for AI development")
    student_model_id: Optional[str] = Field(None, example="zyra-qwen2.5-0.5b-distilled-v1")
    teacher_model: str = Field("zyra-mesh-orchestrator", example="zyra-mesh-orchestrator")
    compare_teacher: bool = Field(True, description="Run both teacher and student simultaneously for comparison")

class DistillationInferenceResponse(BaseModel):
    prompt: str
    student: Dict[str, Any]
    teacher: Optional[Dict[str, Any]] = None
    comparison: Dict[str, Any]

class PricingROIRequest(BaseModel):
    monthly_requests: int = Field(100000, ge=1000, le=100000000)
    avg_prompt_tokens: int = Field(400, ge=50, le=4000)
    avg_completion_tokens: int = Field(600, ge=50, le=4000)
    teacher_cost_per_1m: float = Field(15.0, ge=0.1)

class PricingROIResponse(BaseModel):
    monthly_requests: int
    cloud_teacher_cost_monthly: float
    distilled_model_cost_monthly: float
    net_savings_monthly: float
    savings_percentage: float
    annual_savings: float
    latency_reduction_factor: str
