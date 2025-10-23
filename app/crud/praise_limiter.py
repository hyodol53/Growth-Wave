from typing import List
from sqlalchemy.orm import Session
from app.models.praise_limiter import PraiseLimiter

def get_anonymous_names_for_praisee(db: Session, *, praisee_id: int, evaluation_period: str) -> List[str]:
    """
    Retrieves all existing anonymous names assigned to a specific praisee for the given period.
    """
    return db.query(PraiseLimiter.anonymous_name).filter(
        PraiseLimiter.recipient_id == praisee_id,
        PraiseLimiter.period == evaluation_period,
        PraiseLimiter.anonymous_name.isnot(None)
    ).all()
