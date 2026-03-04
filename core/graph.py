from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from agents.planning_agent import PlanningAgent
from agents.data_agent import DataRetrievalAgent
from agents.forecasting_agent import ForecastingAgent
from agents.analytics_agent import AnalyticsAgent
from agents.decision_agent import DecisionAgent
from agents.explanation_agent import ExplanationAgent

class AgentState(TypedDict):
    """The state of the agentic workflow."""
    query: str
    plan: Dict[str, Any]
    retrieved_data: List[Dict[str, Any]]
    forecast_results: Dict[str, Any]
    kpis: Dict[str, Any]
    recommendation: Dict[str, Any]
    final_explanation: str

class SupplyChainOrchestrator:
    def __init__(self):
        self.planner = PlanningAgent()
        self.data_agent = DataRetrievalAgent()
        self.forecaster = ForecastingAgent()
        self.analytics = AnalyticsAgent()
        self.decision = DecisionAgent()
        self.explainer = ExplanationAgent()
        
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("plan", self.node_plan)
        workflow.add_node("retrieve", self.node_retrieve)
        workflow.add_node("forecast", self.node_forecast)
        workflow.add_node("analyze", self.node_analyze)
        workflow.add_node("optimize", self.node_optimize)
        workflow.add_node("explain", self.node_explain)
        
        # Add edges
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "retrieve")
        workflow.add_edge("retrieve", "forecast")
        workflow.add_edge("forecast", "analyze")
        workflow.add_edge("analyze", "optimize")
        workflow.add_edge("optimize", "explain")
        workflow.add_edge("explain", END)
        
        self.app = workflow.compile()

    def node_plan(self, state: AgentState):
        p = self.planner.plan(state["query"])
        return {"plan": p.dict()}

    def node_retrieve(self, state: AgentState):
        # Simplification: use the first task for now
        sql = self.data_agent.generate_sql(state["query"])
        data = self.data_agent.execute_query(sql.sql)
        return {"retrieved_data": data}

    def node_forecast(self, state: AgentState):
        f = self.forecaster.forecast(state["retrieved_data"])
        return {"forecast_results": f}

    def node_analyze(self, state: AgentState):
        k = self.analytics.calculate_kpis(state["retrieved_data"], state["forecast_results"])
        return {"kpis": k}

    def node_optimize(self, state: AgentState):
        r = self.decision.optimize_inventory(state["kpis"], state["retrieved_data"])
        return {"recommendation": r}

    def node_explain(self, state: AgentState):
        summary = self.explainer.summarize(
            state["query"], 
            state["kpis"], 
            state["forecast_results"], 
            state["recommendation"]
        )
        return {"final_explanation": summary}

    def run(self, query: str):
        return self.app.invoke({"query": query})

if __name__ == "__main__":
    orchestrator = SupplyChainOrchestrator()
    res = orchestrator.run("Which products will run out of stock next week?")
    print(res["final_explanation"])
