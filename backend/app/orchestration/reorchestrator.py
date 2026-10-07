from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.agent import AgentModel
from app.matching.cross_matcher import CrossGraphMatcher
from app.core.logging import logger

class ReOrchestratorEngine:
    """
    Module 12: Dynamic Re-Orchestration Engine.
    Triggered upon agent timeout, schema failure, high uncertainty, or verifier rejection.
    Searches marketplace, hard-filters replacements, ranks candidates using conservative trust,
    selects replacement agent, and reroutes subtask in-flight without restarting the entire workflow.
    """
    def __init__(self):
        self.matcher = CrossGraphMatcher(strategy="ZYRAMESH")

    def find_replacement_agent(
        self,
        db: Session,
        failed_agent_id: str,
        task: Dict[str, Any],
        exclude_agent_ids: List[str]
    ) -> Optional[AgentModel]:
        
        logger.info(f"ReOrchestration triggered for task '{task.get('task_id')}' (Failed agent: {failed_agent_id})")

        all_agents = db.query(AgentModel).filter(AgentModel.status == "ACTIVE").all()
        candidates_pool = [a for a in all_agents if a.agent_id not in exclude_agent_ids and a.agent_id != failed_agent_id]

        eligible, rejections = self.matcher.hard_filter(task, candidates_pool)
        if not eligible:
            logger.warning(f"No eligible replacement candidates found for task '{task.get('task_id')}'")
            return None

        ranked = self.matcher.soft_rank(task, eligible)
        replacement = ranked[0]["agent"]
        logger.info(f"Selected replacement agent '{replacement.name}' ({replacement.agent_id}) for task '{task.get('task_id')}'")
        return replacement
