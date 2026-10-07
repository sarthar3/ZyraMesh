from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.agent import AgentResponse, AgentCreate, AgentUpdate
from app.services.marketplace import (
    list_agents, get_agent_by_id, create_agent, update_agent, delete_agent
)

router = APIRouter(prefix="/agents", tags=["Marketplace Agents"])

@router.get("", response_model=List[AgentResponse])
def get_marketplace_agents(
    capability: Optional[str] = Query(None, description="Filter by capability tag"),
    tool: Optional[str] = Query(None, description="Filter by tool name"),
    category: Optional[str] = Query(None, description="Filter by agent category"),
    agent_status: Optional[str] = Query("ACTIVE", alias="status", description="Filter by agent status"),
    min_trust: Optional[float] = Query(None, description="Filter by minimum trust score"),
    db: Session = Depends(get_db)
):
    return list_agents(
        db,
        capability=capability,
        tool=tool,
        category=category,
        status=agent_status,
        min_trust=min_trust
    )

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent_details(agent_id: str, db: Session = Depends(get_db)):
    agent = get_agent_by_id(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def register_agent(agent_in: AgentCreate, db: Session = Depends(get_db)):
    return create_agent(db, agent_in)

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent_details(agent_id: str, agent_in: AgentUpdate, db: Session = Depends(get_db)):
    updated = update_agent(db, agent_id, agent_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Agent not found")
    return updated

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_agent(agent_id: str, db: Session = Depends(get_db)):
    deleted = delete_agent(db, agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
    return None
