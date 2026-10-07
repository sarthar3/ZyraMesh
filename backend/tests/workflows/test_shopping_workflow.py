import pytest
from app.workflows.shopping_workflow import ShoppingDomainWorkflow

@pytest.mark.asyncio
async def test_shopping_laptop_workflow():
    workflow = ShoppingDomainWorkflow()
    query = "Find the best laptop under ₹70,000 for AI development"
    
    res = await workflow.execute_laptop_recommendation(query, max_budget=70000.0)
    
    assert res["objective"] == query
    assert res["max_budget"] == 70000.0
    assert res["top_recommendation"] is not None
    assert res["top_recommendation"]["name"] == "Lenovo Legion Slim 5"
    assert res["top_recommendation"]["price"] <= 70000.0
    assert "comparison_table" in res
    assert res["verification_status"] == "VERIFIED_PASSED"
