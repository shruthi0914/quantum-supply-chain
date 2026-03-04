import pytest
from agents.planning_agent import PlanningAgent
from agents.data_agent import DataRetrievalAgent

def test_planning_agent_logic():
    planner = PlanningAgent()
    query = "Check inventory for electronics."
    plan = planner.plan(query)
    
    assert plan is not None
    assert len(plan.steps) > 0
    # Ensure at least one step involves data retrieval
    assert any(step.agent_name == "Data Retrieval Agent" for step in plan.steps)

def test_data_agent_sql_generation():
    data_agent = DataRetrievalAgent()
    request = "Total products in category 'health_beauty'"
    result = data_agent.generate_sql(request)
    
    assert "SELECT" in result.sql.upper()
    assert "health_beauty" in result.sql.lower()

def test_forecast_logic_skeleton():
    from agents.forecasting_agent import ForecastingAgent
    forecaster = ForecastingAgent()
    mock_data = [{"date": "2023-01-01", "sales": 100}]
    result = forecaster.forecast(mock_data, periods=3)
    
    assert result["model_used"] == "xgboost"
    assert len(result["forecast"]["predicted_demand"]) == 3

if __name__ == "__main__":
    # Integration style check
    print("Running initial test sanity check...")
    pytest.main([__file__])
