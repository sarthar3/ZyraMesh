import pytest
from app.team_composer.team_composer import ConstrainedTeamComposer
from app.services.marketplace import SEED_AGENTS
from app.models.agent import AgentModel

def test_zyramesh_team_composer():
    agents = [AgentModel(**a) for a in SEED_AGENTS]
    subtasks = [
        {
            "subtask_index": 1,
            "description": "Fetch customer churn records",
            "required_capabilities": ["data_retrieval"],
            "propagation_risk": 0.6
        },
        {
            "subtask_index": 2,
            "description": "Train ML churn classifier",
            "required_capabilities": ["code_execution"],
            "propagation_risk": 0.8
        }
    ]
    composer = ConstrainedTeamComposer(strategy="ZYRAMESH")
    assigned, meta = composer.compose_team(subtasks, agents)
    assert len(assigned) == 2
    assert assigned[0]["assigned_agent_id"] in ["ProductSearchAgent-A", "ProductSearchAgent-B", "agent_data_retriever"]
    assert assigned[1]["assigned_agent_id"] in ["DataAnalysisAgent", "agent_code_executor"]
    assert meta["average_team_fit_score"] > 0
