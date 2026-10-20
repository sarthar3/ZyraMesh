import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.distillation.service import DistillationService
from app.distillation.schemas import DistillationJobCreate

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_distillation_endpoints_list(client):
    """Test listing of initial datasets and distilled models."""
    # Datasets
    res = client.get("/api/v1/distill/datasets")
    assert res.status_code == 200
    datasets = res.json()
    assert len(datasets) >= 1
    assert any("shopping" in d["domain"].lower() for d in datasets)

    # Models
    res_models = client.get("/api/v1/distill/models")
    assert res_models.status_code == 200
    models = res_models.json()
    assert len(models) >= 1
    assert any("qwen" in m["name"].lower() for m in models)

def test_create_and_query_distillation_job(client):
    """Test creation and querying of a Distillation-as-a-Service training job."""
    payload = {
        "name": "Test-Laptop-Distill-Job",
        "description": "Test distillation job",
        "teacher_model": "zyra-mesh-orchestrator",
        "student_base": "qwen2.5:0.5b",
        "distillation_strategy": "SEQUENCE_KD",
        "epochs": 2,
        "batch_size": 2,
        "learning_rate": 2e-5,
        "temperature": 2.0,
        "alpha_kd": 0.7,
        "export_format": "GGUF_Q4_K_M"
    }
    create_res = client.post("/api/v1/distill/jobs", json=payload)
    assert create_res.status_code == 200
    data = create_res.json()
    assert "id" in data
    assert data["name"] == "Test-Laptop-Distill-Job"
    assert data["teacher_latency_ms"] > data["student_latency_ms"]
    assert data["cost_reduction_pct"] > 90.0

    job_id = data["id"]

    # Query detail
    get_res = client.get(f"/api/v1/distill/jobs/{job_id}")
    assert get_res.status_code == 200
    job_detail = get_res.json()
    assert job_detail["id"] == job_id

def test_distillation_inference_arena(client):
    """Test side-by-side inference comparing teacher vs distilled student."""
    infer_payload = {
        "prompt": "Recommend a laptop under ₹70,000 for AI development.",
        "student_model_id": "zyra-qwen2.5-0.5b-distilled-v1",
        "teacher_model": "zyra-mesh-orchestrator",
        "compare_teacher": True
    }
    res = client.post("/api/v1/distill/infer", json=infer_payload)
    assert res.status_code == 200
    res_data = res.json()
    assert "student" in res_data
    assert "teacher" in res_data
    assert "comparison" in res_data
    assert res_data["student"]["latency_ms"] < res_data["teacher"]["latency_ms"]
    assert res_data["comparison"]["cost_reduction_pct"] > 80.0

def test_pricing_roi_calculator(client):
    """Test commercial ROI calculation."""
    res = client.get("/api/v1/distill/roi?monthly_requests=100000&teacher_cost_per_1m=15.0")
    assert res.status_code == 200
    data = res.json()
    assert data["monthly_requests"] == 100000
    assert data["cloud_teacher_cost_monthly"] > data["distilled_model_cost_monthly"]
    assert data["net_savings_monthly"] > 1000.0
    assert data["savings_percentage"] > 90.0

def test_model_export(client):
    """Test export of GGUF metadata and Ollama Modelfile."""
    res = client.get("/api/v1/distill/export/zyra-qwen2.5-0.5b-distilled-v1")
    assert res.status_code == 200
    data = res.json()
    assert "ollama_modelfile" in data
    assert "FROM" in data["ollama_modelfile"]
    assert "curl_snippet" in data
