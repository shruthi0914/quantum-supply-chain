import chromadb
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

class ExplanationAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        # Point to the vector store initialized previously
        db_path = os.path.join(os.getcwd(), "data/vector_store/chroma_db")
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.collection = self.chroma_client.get_or_create_collection(name="supply_chain_knowledge")
        
        self.explanation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Principal Consultant at McKinsey QuantumBlack.
            Synthesize technical AI outputs into an executive summary.
            Use the provided 'Relevant Context' from internal policy docs to justify your answer.
            
            Relevant Context:
            {context}"""),
            ("human", """User Query: {query}
            Metrics: {data_summary}
            Forecast: {forecast_data}
            Recommendation: {optimization_data}""")
        ])

    def retrieve_context(self, query: str) -> str:
        """Retrieves relevant policies/documents from ChromaDB."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=2
            )
            return "\n".join(results['documents'][0]) if results['documents'] and results['documents'][0] else "No specific policy context found."
        except Exception as e:
            print(f"RAG Retrieval Error: {e}")
            return "Context retrieval unavailable."

    def summarize(self, query: str, data: Dict[str, Any], forecast: Dict[str, Any], optimization: Dict[str, Any]) -> str:
        """Generates context-aware summary."""
        context = self.retrieve_context(query)
        chain = self.explanation_prompt | self.llm
        response = chain.invoke({
            "context": context,
            "query": query,
            "data_summary": data,
            "forecast_data": forecast,
            "optimization_data": optimization
        })
        return response.content

if __name__ == "__main__":
    agent = ExplanationAgent()
    print(agent.summarize("What is the reorder policy?", {"kpi": "low"}, {"f": "up"}, {"q": 100}))
