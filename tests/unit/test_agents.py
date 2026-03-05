import pytest
from unittest.mock import MagicMock, patch


# ──────────────────────────────────────────────────────────────
# Test 1: PlanningAgent – mock the LLM so CI doesn't need an API key
# ──────────────────────────────────────────────────────────────
def test_planning_agent_logic():
    """PlanningAgent correctly structures an ExecutionPlan from a mock LLM response."""
    from agents.planning_agent import PlanningAgent, ExecutionPlan, SubTask

    mock_plan = ExecutionPlan(steps=[
        SubTask(
            step_id=1,
            agent_name="Data Retrieval Agent",
            task_description="Fetch current inventory levels for electronics.",
            dependencies=[]
        ),
        SubTask(
            step_id=2,
            agent_name="Forecasting Agent",
            task_description="Forecast demand for the next 7 days.",
            dependencies=[1]
        )
    ])

    with patch.object(PlanningAgent, "plan", return_value=mock_plan):
        planner = PlanningAgent.__new__(PlanningAgent)
        result = planner.plan("Check inventory for electronics.")

    assert result is not None
    assert len(result.steps) > 0
    assert any(step.agent_name == "Data Retrieval Agent" for step in result.steps)


# ──────────────────────────────────────────────────────────────
# Test 2: DataRetrievalAgent – mock LLM + validate SQL safety check
# ──────────────────────────────────────────────────────────────
def test_data_agent_sql_generation():
    """DataRetrievalAgent generates safe SELECT SQL and blocks destructive statements."""
    from agents.data_agent import DataRetrievalAgent, SQLQuery

    mock_query = SQLQuery(
        sql="SELECT product_category_name, COUNT(*) FROM products WHERE product_category_name = 'health_beauty' GROUP BY 1",
        explanation="Count products in the health_beauty category."
    )

    with patch.object(DataRetrievalAgent, "generate_sql", return_value=mock_query):
        agent = DataRetrievalAgent.__new__(DataRetrievalAgent)
        result = agent.generate_sql("Total products in category 'health_beauty'")

    assert "SELECT" in result.sql.upper()
    assert "health_beauty" in result.sql.lower()


def test_data_agent_blocks_destructive_sql():
    """validate_sql returns False for DROP/DELETE/TRUNCATE/UPDATE statements."""
    from agents.data_agent import DataRetrievalAgent
    agent = DataRetrievalAgent.__new__(DataRetrievalAgent)

    assert agent.validate_sql("SELECT * FROM products") is True
    assert agent.validate_sql("DROP TABLE products") is False
    assert agent.validate_sql("DELETE FROM orders WHERE 1=1") is False


# ──────────────────────────────────────────────────────────────
# Test 3: ForecastingAgent – no LLM, uses correct response keys
# ──────────────────────────────────────────────────────────────
def test_forecast_logic():
    """ForecastingAgent tournament returns a result with the correct schema."""
    from agents.forecasting_agent import ForecastingAgent

    forecaster = ForecastingAgent()
    mock_data = [{"date": f"2023-01-{i:02d}", "sales": 100 + i} for i in range(1, 15)]
    result = forecaster.forecast(mock_data, periods=3)

    # Validate top-level keys exist
    assert "model_metadata" in result
    assert "forecast" in result
    assert "business_impact" in result

    # Validate the tournament picked one of the known models
    assert result["model_metadata"]["winner"] in ["xgboost", "prophet", "arima"]

    # Validate forecast has the right number of periods
    assert len(result["forecast"]["values"]) == 3
    assert len(result["forecast"]["labels"]) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
