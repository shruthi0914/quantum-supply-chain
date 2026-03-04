import time
import json
import random

def log_step(agent, message):
    print(f"\n[AGENT: {agent}]")
    print(f"  > {message}")
    time.sleep(1)

def run_demo():
    print("="*60)
    print("  QUANTUM SUPPLY CHAIN AGENT - DEMO RUN (SIMULATED)")
    print("="*60)
    
    query = "Which products are likely to run out of stock next week and how should inventory be optimized?"
    print(f"\nUSER QUERY: \"{query}\"\n")
    
    # 1. Planning Agent
    log_step("Planning Agent", "Decomposing query into sub-tasks...")
    plan = [
        {"id": 1, "task": "Fetch current inventory and category sales", "agent": "Data Retrieval"},
        {"id": 2, "task": "Forecast demand for next 14 days", "agent": "Forecasting"},
        {"id": 3, "task": "Calculate Stockout Risk & Coverage", "agent": "Analytics"},
        {"id": 4, "task": "Generate reorder recommendations (EOQ)", "agent": "Decision"},
        {"id": 5, "task": "Synthesize executive summary", "agent": "Explanation"}
    ]
    print(json.dumps(plan, indent=4))

    # 2. Data Retrieval
    log_step("Data Retrieval Agent", "Executing SQL: SELECT p.category, i.stock, s.recent_sales FROM products p JOIN inventory i ON p.id = i.id...")
    data = {"category": "health_beauty", "current_stock": 150, "avg_daily_sales": 25}
    print(f"  Retrieved Data: {data}")

    # 3. Forecasting
    log_step("Forecasting Agent", "Running model tournament (XGBoost vs Prophet)...")
    log_step("Forecasting Agent", "Winner: XGBoost. Predicted demand for next 7 days: 210 units (Trend: +15%).")
    forecast = 210

    # 4. Analytics
    log_step("Analytics Agent", "Calculating KPIs...")
    coverage = data['current_stock'] / (forecast / 7)
    risk = 0.45 if coverage < 7 else 0.05
    print(f"  Stockout Risk: {risk*100}%")
    print(f"  Inventory Coverage: {coverage:.2f} days")

    # 5. Decision
    log_step("Decision Agent", "Optimizing reorder quantities via EOQ logic...")
    recommendation = {"action": "REORDER", "quantity": 500, "priority": "CRITICAL"}
    print(f"  Recommendation: {recommendation}")

    # 6. Explanation
    log_step("Explanation Agent", "Synthesizing executive summary...")
    summary = """
    EXECUTIVE SUMMARY:
    Our AI-driven analysis indicates a CRITICAL stockout risk (45%) for the 'health_beauty' category within the next 7 days.
    Current inventory is 150 units, but our XGBoost model forecasts a demand surge to 210 units due to seasonal trends.
    
    RECOMMENDATION:
    - Initiate immediate REORDER of 500 units.
    - This aligns with internal Policy A (Safety Stock > 7 days).
    - Expected Impact: 95% service level maintained and 12% reduction in stockout-related revenue loss.
    """
    print(summary)
    
    print("="*60)
    print("  DEMO RUN COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_demo()
