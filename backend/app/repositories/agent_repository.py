from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.agent import AgentModel

class AgentRepository(BaseRepository[AgentModel]):
    def __init__(self, db: Session):
        super().__init__(AgentModel, db)

    def find_by_capability(self, capability: str) -> List[AgentModel]:
        all_agents = self.db.query(AgentModel).filter(AgentModel.status == "ACTIVE").all()
        return [a for a in all_agents if capability in a.capabilities]

    def get_available(self) -> List[AgentModel]:
        return self.db.query(AgentModel).filter(
            AgentModel.status == "ACTIVE",
            AgentModel.availability_status == "AVAILABLE"
        ).all()
