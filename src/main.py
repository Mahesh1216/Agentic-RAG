from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from src.rag_pipeline import create_retriever, get_rag_response, get_llm_response, agentic_search

# Initialize FastAPI
app = FastAPI()

# Pydantic model for request body
class ChatRequest(BaseModel):
    query: str
    type: str = "rag"  # Default is "rag"; if "llm", use LLM directly

# Initialize the RAG pipeline once
print("Initializing RAG pipeline...")
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
retriever = create_retriever()
print("RAG pipeline initialized successfully.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Boss Wallah Chatbot API! Use the /chat endpoint to get started."}

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Single POST endpoint that chooses between RAG or LLM based on request type.
    """
    try:
        if request.type.lower() == "llm":
            # Use LLM only
            answer = get_llm_response(request.query)
        else:
            # Use RAG retriever + LLM, with agentic fallback
            answer = agentic_search(retriever, request.query)
        
        return {"query": request.query, "type": request.type, "response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent-chat")
def agent_chat(request: ChatRequest):
    """
    An endpoint that uses an agentic approach to answer questions.
    """
    try:
        answer = agentic_search(retriever, request.query)
        return {"query": request.query, "type": "agent", "response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
