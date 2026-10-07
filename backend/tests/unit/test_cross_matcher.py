import pytest
from app.matching.cross_matcher import CrossGraphMatcher
from app.models.agent import AgentModel
from app.services.marketplace import SEED_AGENTS

def test_stage_1_hard_filtering_and_stage_2_conservative_trust_ranking():
    agents = [AgentModel(**a) for a in SEED_AGENTS]
    matcher = CrossGraphMatcher(k_uncertainty=0.5, strategy="ZYRAMESH")
    
    task = {
        "task_id": "task_spec",
        "description": "Extract laptop hardware specs",
        "required_capabilities": ["specification_analysis"],
        "propagation_risk": 0.8
    }

    # Stage 1: Hard Filter
    eligible, rejections = matcher.hard_filter(task, agents, max_latency_ms=300)
    assert len(eligible) >= 2

    # Stage 2: Soft Rank with Conservative Trust
    ranked = matcher.soft_rank(task, eligible)
    assert len(ranked) >= 2
    top = ranked[0]
    
    assert top["agent"].agent_id in ["SpecificationAgent-A", "SpecificationAgent-B"]
    assert top["conservative_trust"] > 0
    assert "explanation" in top
