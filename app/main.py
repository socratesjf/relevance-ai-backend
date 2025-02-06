from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI
from datetime import datetime

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
class AgentDetails(BaseModel):
    id: str = Field(description="The unique identifier of the agent")
    name: str = Field(description="The name of the agent")
    status: str = Field(description="Current status of the agent", default="active")
    lastActive: str = Field(description="Last active timestamp", default="")
    tasksCompleted: int = Field(description="Number of completed tasks", default=0)
    successRate: float = Field(description="Success rate of completed tasks", default=0)
    currentTask: str = Field(description="Current task being processed", default="")

# Routes
@app.get("/")
async def root():
    return {"message": "Relevance AI Backend API"}

@app.get("/agents/details", response_model=List[AgentDetails])
async def get_agents_details():
    try:
        agents = client.agents.list_agents()
        agent_details = []
        
        for agent in agents:
            agent_details.append(
                AgentDetails(
                    id=agent.agent_id,
                    name=agent.metadata.name,  # Access name from metadata object
                    status="active",
                    lastActive="",
                    tasksCompleted=0,
                    successRate=0,
                    currentTask=""
                )
            )
        
        return agent_details
    except Exception as e:
        print(f"Error in get_agents_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/{agent_id}", response_model=AgentDetails)
async def get_agent(agent_id: str):
    try:
        agent = client.agents.retrieve_agent(agent_id=agent_id)
        return AgentDetails(
            id=agent.agent_id,
            name=agent.metadata.name,  # Access name from metadata object
            status="active",
            lastActive="",
            tasksCompleted=0,
            successRate=0,
            currentTask=""
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Agent not found: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)