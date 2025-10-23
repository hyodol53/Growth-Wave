from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from collections import Counter

from app import models, schemas
from app.crud.base import CRUDBase
from app.models import User, Praise, PraiseLimiter, Strength
from app.schemas.praise import PraiseCreate
from app.schemas.strength import StrengthStat
from app.utils.anonymous_names import generate_anonymous_name
from app.exceptions import PraiseLimitExceeded
import datetime

# TODO: This should be configurable via a settings page as per NFR-6
PRAISE_LIMIT_PER_PERIOD = 5

def get_current_period() -> str:
    """Determines the current evaluation period (e.g., 2024-H1)."""
    now = datetime.datetime.now()
    half = "H1" if now.month < 7 else "H2"
    return f"{now.year}-{half}"

def create_praise(db: Session, *, praise_in: PraiseCreate, sender_id: int, strengths: list[Strength]) -> Praise:
    period = get_current_period()

    # 1. Find or create the praise limiter record
    limiter = db.query(models.PraiseLimiter).filter(
        models.PraiseLimiter.sender_id == sender_id,
        models.PraiseLimiter.recipient_id == praise_in.recipient_id,
        models.PraiseLimiter.period == period
    ).first()

    if limiter and limiter.count >= PRAISE_LIMIT_PER_PERIOD:
        raise PraiseLimitExceeded()

    if limiter:
        # Record exists, check for anonymous name
        if not limiter.anonymous_name:
            # If name is missing (e.g., old data), generate and save it
            limiter.anonymous_name = generate_anonymous_name(db, praisee_id=praise_in.recipient_id, evaluation_period=period)
        limiter.count += 1
    else:
        # No record, create a new one
        new_name = generate_anonymous_name(db, praisee_id=praise_in.recipient_id, evaluation_period=period)
        limiter = models.PraiseLimiter(
            sender_id=sender_id,
            recipient_id=praise_in.recipient_id,
            period=period,
            count=1,
            anonymous_name=new_name
        )
        db.add(limiter)
    
    db.commit()
    db.refresh(limiter)

    anonymous_name_to_use = limiter.anonymous_name

    # 2. Create the praise object
    # Note: sender_id is intentionally not saved in the Praise model to ensure anonymity
    db_praise = Praise(
        recipient_id=praise_in.recipient_id,
        message=praise_in.message,
        anonymous_name=anonymous_name_to_use,
        strengths=strengths
    )
    db.add(db_praise)
    db.commit()
    db.refresh(db_praise)
    return db_praise

def get_praises_for_user(db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> list[Praise]:
    return db.query(Praise).filter(Praise.recipient_id == user_id).order_by(Praise.created_at.desc(), Praise.id.desc()).offset(skip).limit(limit).all()

def get_strength_profile_for_user(db: Session, *, user: User) -> list[StrengthStat]:
    praises = user.praises_received
    if not praises:
        return []

    all_hashtags = [strength.hashtag for praise in praises for strength in praise.strengths]
    hashtag_counts = Counter(all_hashtags)

    strength_stats = [StrengthStat(hashtag=h, count=c) for h, c in hashtag_counts.items()]
    # Sort by count descending, then alphabetically
    strength_stats.sort(key=lambda x: (-x.count, x.hashtag))

    return strength_stats
