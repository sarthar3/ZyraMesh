from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from app.database import get_db
from app.schemas.eval import BenchmarkRunRequest, BenchmarkMetricResponse
from app.services.evaluator import EvaluatorEngine
from app.models.audit import BenchmarkMetricModel

router = APIRouter(prefix="/eval", tags=["Evaluation & Benchmarking"])

class StressTestRequest(BaseModel):
    agent_counts: List[int] = [10, 25, 50, 100, 250]
    seed: int = 42

class AblationRunRequest(BaseModel):
    num_samples: int = 10
    seed: int = 42

@router.post("/run", response_model=List[BenchmarkMetricResponse])
def run_evaluation_benchmark(req: BenchmarkRunRequest, db: Session = Depends(get_db)):
    evaluator = EvaluatorEngine()
    metrics = evaluator.run_benchmark_suite(db, num_samples=req.num_samples)
    return metrics

@router.post("/ablation", response_model=List[BenchmarkMetricResponse])
def run_ablation_benchmark(req: AblationRunRequest, db: Session = Depends(get_db)):
    evaluator = EvaluatorEngine()
    metrics = evaluator.run_ablation_study(db, num_samples=req.num_samples, seed=req.seed)
    return metrics

@router.post("/stress")
def run_stress_test(req: StressTestRequest):
    evaluator = EvaluatorEngine()
    return evaluator.run_stress_test(agent_counts=req.agent_counts, seed=req.seed)

@router.get("/metrics", response_model=List[BenchmarkMetricResponse])
def get_evaluation_metrics(db: Session = Depends(get_db)):
    return db.query(BenchmarkMetricModel).order_by(BenchmarkMetricModel.timestamp.desc()).limit(100).all()

@router.get("/export/csv")
def export_metrics_as_csv(db: Session = Depends(get_db)):
    metrics = db.query(BenchmarkMetricModel).order_by(BenchmarkMetricModel.timestamp.desc()).all()
    csv_data = EvaluatorEngine.export_metrics_csv(metrics)
    return Response(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=zyra_evaluation_results.csv"})

@router.get("/export/json")
def export_metrics_as_json(db: Session = Depends(get_db)):
    metrics = db.query(BenchmarkMetricModel).order_by(BenchmarkMetricModel.timestamp.desc()).all()
    return [
        {
            "metric_id": m.metric_id,
            "run_id": m.run_id,
            "strategy": m.strategy,
            "ablation": m.ablation,
            "workflow_success_rate": m.workflow_success_rate,
            "failure_propagation_rate": m.failure_propagation_rate,
            "expected_calibration_error": m.expected_calibration_error,
            "avg_latency_ms": m.avg_latency_ms,
            "total_cost": m.total_cost,
            "verification_frequency": m.verification_frequency,
            "rerouting_success_rate": m.rerouting_success_rate,
            "policy_violations_count": m.policy_violations_count,
            "sample_size": m.sample_size,
            "timestamp": m.timestamp.isoformat() if m.timestamp else None
        } for m in metrics
    ]
