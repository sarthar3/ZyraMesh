from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models.agent import AgentModel
from app.models.trust import TrustObservationModel
from app.schemas.trust import TrustObservationResponse, AgentTrustLeaderboardItem

router = APIRouter(prefix="/trust", tags=["Trust Analytics & Observations"])

@router.get("/leaderboard", response_model=List[AgentTrustLeaderboardItem])
def get_trust_leaderboard(db: Session = Depends(get_db)):
    agents = db.query(AgentModel).all()
    leaderboard = []
    
    for a in agents:
        obs_count = db.query(TrustObservationModel).filter(TrustObservationModel.agent_id == a.agent_id).count()
        succ_count = db.query(TrustObservationModel).filter(
            TrustObservationModel.agent_id == a.agent_id,
            TrustObservationModel.success == True
        ).count()
        
        succ_rate = round(succ_count / max(1, obs_count), 4) if obs_count > 0 else 0.85
        
        item = AgentTrustLeaderboardItem(
            agent_id=a.agent_id,
            name=a.name,
            trust_mean=a.trust_mean,
            trust_uncertainty=a.trust_uncertainty,
            capability_trust=a.capability_specific_trust or {},
            total_executions=obs_count,
            success_rate=succ_rate
        )
        leaderboard.append(item)
        
    leaderboard.sort(key=lambda x: x.trust_mean, reverse=True)
    return leaderboard

@router.get("/observations", response_model=List[TrustObservationResponse])
def get_trust_observations(agent_id: str = None, db: Session = Depends(get_db)):
    query = db.query(TrustObservationModel)
    if agent_id:
        query = query.filter(TrustObservationModel.agent_id == agent_id)
    return query.order_by(TrustObservationModel.timestamp.desc()).limit(50).all()
