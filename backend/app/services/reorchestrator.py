from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.agent import AgentModel

class ReOrchestratorEngine:
    """
    Dynamic Re-Orchestration Engine for ZyraMesh.
    Identifies alternative candidate agents upon task failure or verification rejection.
    """
    def find_replacement_agent(
        self,
        db: Session,
        failed_agent_id: str,
        task: Dict[str, Any],
        exclude_agent_ids: List[str]
    ) -> Optional[AgentModel]:
        
        req_caps = set(task.get("required_capabilities", []))
        all_agents = db.query(AgentModel).filter(AgentModel.status == "ACTIVE").all()
        
        candidates = []
        for agent in all_agents:
            if agent.agent_id in exclude_agent_ids or agent.agent_id == failed_agent_id:
                continue
            if agent.availability_status == "OFFLINE":
                continue
            
            agent_caps = set(agent.capabilities)
            if req_caps.intersection(agent_caps):
                candidates.append(agent)

        if not candidates:
            return None
        
        # Sort candidate by highest trust mean
        candidates.sort(key=lambda a: a.trust_mean, reverse=True)
        return candidates[0]
