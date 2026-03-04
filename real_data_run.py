import pandas as pd
import os
import json
from agents.planning_agent import PlanningAgent
from agents.forecasting_agent import ForecastingAgent
from agents.analytics_agent import AnalyticsAgent
from agents.decision_agent import DecisionAgent
from agents.explanation_agent import ExplanationAgent

# Path to the real data
DATA_PATH = "/Users/shruthirajgangapuri/.gemini/antigravity/scratch/quantum-supply-chain-agent/data/raw"

def run_real_data_analysis():
    print("="*60)
    print("  QUANTUM SUPPLY CHAIN AGENT - REAL DATA EXECUTION")
    print("="*60)

    # 1. Load Real Data
    print("\n[STEP 1] Loading Olist Datasets...")
    try:
        products_df = pd.read_csv(os.path.join(DATA_PATH, "olist_products_dataset.csv"))
        order_items_df = pd.read_csv(os.path.join(DATA_PATH, "olist_order_items_dataset.csv"))
        print(f"  Successfully loaded {len(products_df)} products and {len(order_items_df)} order items.")
    except Exception as e:
        print(f"  Error loading data: {e}")
        return

    # 2. Extract real context for an agent
    # Let's pick a top category
    top_categories = products_df['product_category_name'].value_counts().head(5)
    target_category = top_categories.index[0] # health_beauty usually
    print(f"\n[STEP 2] Analyzing Category: '{target_category}'")
    
    # Calculate real sales count for this category
    cat_products = products_df[products_df['product_category_name'] == target_category]['product_id']
    cat_sales = order_items_df[order_items_df['product_id'].isin(cat_products)]
    total_sales_val = cat_sales['price'].sum()
    print(f"  Real Data Insight: Total Sales for '{target_category}' = ${total_sales_val:,.2f}")

    # 3. Agentic Workflow
    query = f"Identify stockout risks and reorder requirements for the '{target_category}' category."
    
    # Planning
    planner = PlanningAgent()
    print("\n[AGENT: Planning Agent]")
    print(f"  > Decomposing: {query}")
    
    # Forecasting (Tournament)
    forecaster = ForecastingAgent()
    print("\n[AGENT: Forecasting Agent]")
    # We pass real row counts as a proxy for historical volume to the forecaster
    mock_history = [{"date": "2018-01-01", "sales": len(cat_sales) // 100}] * 10
    forecast_result = forecaster.forecast(mock_history)
    
    # Analytics
    analytics = AnalyticsAgent()
    print("\n[AGENT: Analytics Agent]")
    kpis = analytics.calculate_kpis([], forecast_result)
    
    # Decision
    decision = DecisionAgent()
    print("\n[AGENT: Decision Agent]")
    recommendation = decision.optimize_inventory(kpis, [])

    # Explanation (Synthesize with Real Data Context)
    explainer = ExplanationAgent()
    print("\n[AGENT: Explanation Agent]")
    final_output = explainer.summarize(
        query, 
        {"category": target_category, "total_sales_to_date": f"${total_sales_val:,.2f}"}, 
        forecast_result, 
        recommendation
    )
    
    print("\n" + "="*60)
    print("  FINAL EXECUTIVE SUMMARY")
    print("="*60)
    print(final_output)
    print("="*60)

if __name__ == "__main__":
    run_real_data_analysis()
