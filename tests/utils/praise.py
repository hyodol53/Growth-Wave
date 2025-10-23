from sqlalchemy.orm import Session
from typing import List

from app import crud, models
from app.utils.anonymous_names import generate_anonymous_name
from app.crud.praise import get_current_period

def create_random_praise(
    db: Session, *, sender: models.User, recipient: models.User, hashtags: List[str], message: str = "random message"
) -> models.Praise:
    """
    Test utility to create a praise record directly in the DB.
    """
    # 1. Get or create Strength objects
    strength_objects = crud.strength.get_or_create_strengths_by_hashtags(db, hashtags=hashtags)

    # 2. Get or create a consistent anonymous name via PraiseLimiter
    period = get_current_period()
    limiter = db.query(models.PraiseLimiter).filter(
        models.PraiseLimiter.sender_id == sender.id,
        models.PraiseLimiter.recipient_id == recipient.id,
        models.PraiseLimiter.period == period
    ).first()

    if not limiter:
        anon_name = generate_anonymous_name(db, praisee_id=recipient.id, evaluation_period=period)
        limiter = models.PraiseLimiter(
            sender_id=sender.id,
            recipient_id=recipient.id,
            period=period,
            count=0, # We don't care about the count for this utility
            anonymous_name=anon_name
        )
        db.add(limiter)
        db.commit()
        db.refresh(limiter)

    # 3. Create the Praise object
    praise = models.Praise(
        recipient_id=recipient.id,
        message=message,
        anonymous_name=limiter.anonymous_name,
        strengths=strength_objects,
    )
    db.add(praise)
    db.commit()
    db.refresh(praise)
    return praise
