import pytest
import asyncio
from app.services.objective_analyzer import ObjectiveAnalyzer
from app.services.actg_builder import ACTGBuilder
from app.services.marketplace import SEED_AGENTS
from app.models.agent import AgentModel

@pytest.mark.asyncio
async def test_tdg_construction():
    analyzer = ObjectiveAnalyzer(provider_name="mock")
    subtasks, tdg_json = await analyzer.analyze_objective("Analyze customer churn database and build predictive ML model")
    assert len(subtasks) > 0
    assert "nodes" in tdg_json
    assert "edges" in tdg_json

def test_actg_construction():
    agents = [AgentModel(**a) for a in SEED_AGENTS]
    g, actg_json = ACTGBuilder.build_actg(agents)
    assert len(actg_json["nodes"]) > 0
    assert len(actg_json["edges"]) > 0
