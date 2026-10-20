from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.distillation.schemas import (
    DistillationJobCreate,
    DistillationJobResponse,
    DistillationJobDetail,
    DatasetGenerateRequest,
    DistillationDatasetResponse,
    DistilledModelResponse,
    DistillationInferenceRequest,
    DistillationInferenceResponse,
    PricingROIResponse
)
from app.distillation.service import DistillationService
from app.distillation.dataset_generator import generate_synthetic_dataset

router = APIRouter(prefix="/distill", tags=["Distillation as a Service (DaaS)"])

@router.post("/jobs", response_model=DistillationJobResponse)
def create_distillation_job(data: DistillationJobCreate, db: Session = Depends(get_db)):
    """
    Launch a new Distillation-as-a-Service (DaaS) training run.
    Compresses heavy multi-agent or frontier LLM intelligence into an edge-deployable compact student.
    """
    return DistillationService.create_job(data, db)

@router.get("/jobs", response_model=List[DistillationJobResponse])
def list_distillation_jobs(db: Session = Depends(get_db)):
    """List all knowledge distillation training jobs with status and progress."""
    return DistillationService.list_jobs(db)

@router.get("/jobs/{job_id}", response_model=DistillationJobDetail)
def get_distillation_job(job_id: str, db: Session = Depends(get_db)):
    """Get detailed telemetry, loss curves, and artifact exports for a distillation job."""
    job = DistillationService.get_job(job_id, db)
    if not job:
        raise HTTPException(status_code=404, detail="Distillation job not found")
    return job

@router.post("/jobs/{job_id}/cancel", response_model=DistillationJobResponse)
def cancel_distillation_job(job_id: str, db: Session = Depends(get_db)):
    """Cancel an active distillation job."""
    job = DistillationService.cancel_job(job_id, db)
    if not job:
        raise HTTPException(status_code=404, detail="Distillation job not found or cannot be cancelled")
    return job

@router.post("/generate-dataset", response_model=DistillationDatasetResponse)
async def generate_dataset(data: DatasetGenerateRequest, db: Session = Depends(get_db)):
    """
    Synthesize high-fidelity distillation data using the Teacher model.
    Automatically applies Zyra's Uncertainty Gate to filter out hallucinated traces.
    """
    dataset = await generate_synthetic_dataset(
        name=data.name,
        domain=data.domain,
        num_samples=data.num_samples,
        teacher_source=data.teacher_source,
        uncertainty_threshold=data.uncertainty_threshold,
        db=db
    )
    return dataset

@router.get("/datasets", response_model=List[DistillationDatasetResponse])
def list_datasets(db: Session = Depends(get_db)):
    """List all available distillation datasets."""
    return DistillationService.list_datasets(db)

@router.get("/models", response_model=List[DistilledModelResponse])
def list_distilled_models(db: Session = Depends(get_db)):
    """List all registered, deploy-ready distilled student models."""
    return DistillationService.list_models(db)

@router.post("/infer", response_model=DistillationInferenceResponse)
async def run_inference(data: DistillationInferenceRequest, db: Session = Depends(get_db)):
    """
    Real-Time DaaS Inference Arena.
    Runs distilled model on edge vs cloud multi-agent teacher simultaneously to benchmark latency, cost, and fidelity.
    """
    return await DistillationService.run_side_by_side_inference(
        prompt=data.prompt,
        student_model_id=data.student_model_id,
        teacher_model=data.teacher_model,
        compare_teacher=data.compare_teacher,
        db=db
    )

@router.get("/roi", response_model=PricingROIResponse)
def get_pricing_roi(
    monthly_requests: int = Query(100000, ge=1000, le=100000000),
    avg_prompt_tokens: int = Query(400, ge=50, le=4000),
    avg_completion_tokens: int = Query(600, ge=50, le=4000),
    teacher_cost_per_1m: float = Query(15.0, ge=0.1)
):
    """Calculate commercial ROI and enterprise cost savings achieved by deploying the distilled model."""
    return DistillationService.calculate_roi(
        monthly_requests=monthly_requests,
        avg_prompt_tokens=avg_prompt_tokens,
        avg_completion_tokens=avg_completion_tokens,
        teacher_cost_per_1m=teacher_cost_per_1m
    )

@router.get("/export/{model_id}")
def export_model_artifacts(model_id: str, db: Session = Depends(get_db)):
    """Export Ollama Modelfile and GGUF deployment instructions."""
    models = DistillationService.list_models(db)
    matched = next((m for m in models if m.id == model_id or model_id in m.id), None)
    
    model_name = matched.name if matched else "Zyra-Distilled-Model"
    base_arch = matched.base_architecture if matched else "qwen2.5:0.5b"
    
    modelfile_content = (
        f"# ============================================================\n"
        f"# Zyra Mesh - Distillation as a Service (DaaS) Production Export\n"
        f"# Model: {model_name}\n"
        f"# Base Architecture: {base_arch}\n"
        f"# Format: GGUF Quantized (Q4_K_M)\n"
        f"# ============================================================\n\n"
        f"FROM {base_arch}\n"
        f"PARAMETER temperature 0.3\n"
        f"PARAMETER top_p 0.9\n"
        f"PARAMETER stop \"<|im_end|>\"\n\n"
        f"SYSTEM \"\"\"\n"
        f"You are {model_name}, a high-efficiency student model distilled from Zyra Mesh Multi-Agent Architecture.\n"
        f"You produce structured, verified domain decisions in a single sub-60ms forward pass.\n"
        f"\"\"\"\n"
    )
    
    curl_snippet = (
        f"# Production Real-Time Inference cURL:\n"
        f"curl -X POST \"http://localhost:8000/api/v1/distill/infer\" \\\n"
        f"  -H \"Content-Type: application/json\" \\\n"
        f"  -d '{{\"prompt\": \"Find best laptop under ₹70,000 for AI development\", \"student_model_id\": \"{model_id}\"}}'\n"
    )

    return {
        "model_id": model_id,
        "model_name": model_name,
        "format": "GGUF_Q4_K_M",
        "size_mb": matched.model_size_mb if matched else 394.0,
        "ollama_modelfile": modelfile_content,
        "curl_snippet": curl_snippet,
        "deploy_commands": [
            f"echo '{modelfile_content}' > Modelfile",
            f"ollama create zyra-distilled -f Modelfile",
            f"ollama run zyra-distilled"
        ]
    }
