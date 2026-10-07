import datetime
from sqlalchemy.orm import Session
from app.models.collaboration import CollaborationMemoryModel

class CollaborationMemoryManager:
    """
    Module 14: Pairwise Collaboration Memory Manager.
    Tracks handoff success, schema compatibility, and verifier agreement for Agent A -> Agent B handoffs.
    """
    @staticmethod
    def record_handoff(
        db: Session,
        source_agent_id: str,
        target_agent_id: str,
        success: bool,
        schema_compatible: bool = True,
        verifier_agreed: bool = True,
        latency_ms: float = 0.0
    ) -> CollaborationMemoryModel:
        
        pair_id = f"{source_agent_id}->{target_agent_id}"
        record = db.query(CollaborationMemoryModel).filter(CollaborationMemoryModel.pair_id == pair_id).first()

        if not record:
            record = CollaborationMemoryModel(
                pair_id=pair_id,
                source_agent_id=source_agent_id,
                target_agent_id=target_agent_id,
                successful_handoffs=1 if success else 0,
                failed_handoffs=0 if success else 1,
                schema_compatibility_rate=1.0 if schema_compatible else 0.5,
                verifier_agreement_rate=1.0 if verifier_agreed else 0.5,
                average_handoff_latency_ms=latency_ms,
                compatibility_score=0.95 if success else 0.50,
                updated_at=datetime.datetime.utcnow()
            )
            db.add(record)
        else:
            if success:
                record.successful_handoffs += 1
            else:
                record.failed_handoffs += 1

            total = record.successful_handoffs + record.failed_handoffs
            success_rate = record.successful_handoffs / max(1, total)

            # Update rolling compatibility score
            alpha = 0.20
            score_delta = 1.0 if (success and schema_compatible and verifier_agreed) else 0.20
            record.compatibility_score = round(record.compatibility_score + alpha * (score_delta - record.compatibility_score), 4)
            record.updated_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_compatibility(db: Session, source_agent_id: str, target_agent_id: str) -> float:
        pair_id = f"{source_agent_id}->{target_agent_id}"
        record = db.query(CollaborationMemoryModel).filter(CollaborationMemoryModel.pair_id == pair_id).first()
        return record.compatibility_score if record else 0.85
