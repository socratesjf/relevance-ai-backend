from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Relevance AI Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Relevance AI client
try:
    client = RelevanceAI(
        api_key=os.getenv("RAI_API_KEY"),
        region=os.getenv("RAI_REGION"),
        project=os.getenv("RAI_PROJECT")
    )
except Exception as e:
    print(f"Error initializing Relevance AI client: {e}")
    raise

# Models
class Agent(BaseModel):
    agent_id: str
    name: str
    description: Optional[str] = None

# Routes
@app.get("/")
async def root():
    return {"message": "Relevance AI Backend API"}

@app.get("/agents", response_model=List[Agent])
async def list_agents():
    try:
        agents = client.agents.list_agents()
        return [
            Agent(
                agent_id=agent.agent_id,
                name=agent.name,
                description=getattr(agent, 'description', None)
            )
            for agent in agents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    try:
        agent = client.agents.retrieve_agent(agent_id=agent_id)
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "description": getattr(agent, 'description', None)
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Agent not found: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)