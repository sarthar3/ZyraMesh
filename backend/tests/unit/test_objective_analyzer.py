import pytest
from app.services.objective_analyzer import ObjectiveAnalyzer

@pytest.mark.asyncio
async def test_laptop_shopping_objective_parsing():
    analyzer = ObjectiveAnalyzer(provider_name="mock")
    prompt = "Find the best laptop under ₹70,000 for AI development."
    
    analysis, subtasks, tdg_json = await analyzer.parse_and_decompose(prompt)
    
    assert analysis["category"] == "shopping"
    assert analysis["constraints"].get("max_budget") == 70000.0
    assert len(subtasks) == 5
    assert subtasks[0]["required_capabilities"] == ["product_search", "data_retrieval"]
    assert "nodes" in tdg_json
    assert "edges" in tdg_json
