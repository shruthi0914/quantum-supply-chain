from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.graph import SupplyChainOrchestrator
import uvicorn

app = FastAPI(title="Quantum Supply Chain Agent API")
orchestrator = SupplyChainOrchestrator()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    result: str

@app.post("/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest):
    try:
        res = orchestrator.run(request.query)
        return {
            "query": request.query,
            "result": res["final_explanation"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
