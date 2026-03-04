import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

class SubTask(BaseModel):
    """A sub-task to be executed by a specialized agent."""
    step_id: int = Field(description="The unique ID of the step.")
    agent_name: str = Field(description="The name of the agent to execute this task (Data Retrieval, Forecasting, Analytics, Decision, Explanation).")
    task_description: str = Field(description="Detailed description of what the agent needs to do.")
    dependencies: List[int] = Field(description="List of step IDs that must be completed before this task can start.", default_factory=list)

class ExecutionPlan(BaseModel):
    """The full decomposition of the user query into steps."""
    steps: List[SubTask] = Field(description="Sequence of tasks required to answer the query.")

class PlanningAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.planner_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are the Senior Planning Agent at McKinsey QuantumBlack. 
            Decompose high-level supply chain queries into a structured execution plan.
            Specialized Agents available:
            1. Data Retrieval Agent: Fetches SQL data (Orders, Products, etc.).
            2. Forecasting Agent: Runs time-series models (XGBoost, Prophet).
            3. Analytics Agent: Computes business KPIs (Stockout risk, coverage).
            4. Decision Agent: Generates optimized reorder logic.
            5. Explanation Agent: Synthesizes findings with RAG context.
            
            Format your response as a logical graph of steps."""),
            ("human", "User Query: {query}")
        ])

    def plan(self, query: str) -> ExecutionPlan:
        """Decomposes the query into an ExecutionPlan."""
        # In a real implementation, we would bind the tool or structured output
        planner_chain = self.planner_prompt | self.llm.with_structured_output(ExecutionPlan)
        return planner_chain.invoke({"query": query})

if __name__ == "__main__":
    # Quick test
    planner = PlanningAgent()
    sample_query = "Which products are likely to run out of stock next week and how should inventory be optimized?"
    result = planner.plan(sample_query)
    print(result.json(indent=2))
