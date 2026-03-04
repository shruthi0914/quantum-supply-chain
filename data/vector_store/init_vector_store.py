import chromadb
from chromadb.utils import embedding_functions
import os

# Configuration
CHROMA_PATH = "data/vector_store/chroma_db"

def init_vector_store():
    """Initializes the ChromaDB vector store with supply chain knowledge."""
    try:
        if not os.path.exists(CHROMA_PATH):
            os.makedirs(CHROMA_PATH)
            
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_or_create_collection(name="supply_chain_knowledge")
        
        # Mock documents (Internal policies, best practices)
        docs = [
            "Inventory Policy A: Reorder safety stock when coverage drops below 7 days.",
            "Market Report 2024: Electronics category expected to see 20% growth in Q3.",
            "Supplier Handbook: Lead time for International sellers is average 15 days.",
            "Cost Optimization: Holding costs should not exceed 10% of total inventory value."
        ]
        
        ids = [f"policy_{i}" for i in range(len(docs))]
        
        print(f"Adding {len(docs)} documents to vector store at {CHROMA_PATH}...")
        collection.add(
            documents=docs,
            ids=ids
        )
        print("Vector store initialization complete.")
    except Exception as e:
        print(f"Error initializing vector store: {e}")

if __name__ == "__main__":
    init_vector_store()
