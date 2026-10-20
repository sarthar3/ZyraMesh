from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.agents import router as agents_router
from app.api.v1.workflows import router as workflows_router
from app.api.v1.executions import router as executions_router
from app.api.v1.trust import router as trust_router
from app.api.v1.eval import router as eval_router
from app.api.v1.websocket import router as ws_router
from app.api.v1.auth import router as auth_router
from app.api.v1.simulation import router as simulation_router
from app.api.v1.stats import router as stats_router
from app.api.v1.distill import router as distill_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(agents_router)
api_v1_router.include_router(workflows_router)
api_v1_router.include_router(executions_router)
api_v1_router.include_router(trust_router)
api_v1_router.include_router(eval_router)
api_v1_router.include_router(ws_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(simulation_router)
api_v1_router.include_router(stats_router)
api_v1_router.include_router(distill_router)

