from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter
import random

from app.models import User, Praise, PraiseLimiter, Strength
from app.schemas.praise import PraiseCreate
from app.schemas.strength import StrengthStat

# List of anonymous animals for praise sender
ANONYMOUS_ANIMALS = ["익명의 고라니", "익명의 다람쥐", "익명의 토끼", "익명의 부엉이", "익명의 사자", "익명의 호랑이"]

def get_current_period() -> str:
    """Determines the current evaluation period (e.g., 2024-H1)."""
    from datetime import datetime
    now = datetime.now()
    half = "H1" if now.month < 7 else "H2"
    return f"{now.year}-{half}"

def get_praise_limiter(db: Session, *, sender_id: int, recipient_id: int) -> PraiseLimiter | None:
    period = get_current_period()
    return db.query(PraiseLimiter).filter_by(sender_id=sender_id, recipient_id=recipient_id, period=period).first()

def upsert_praise_limiter(db: Session, *, limiter: PraiseLimiter | None, sender_id: int, recipient_id: int) -> PraiseLimiter:
    period = get_current_period()
    if limiter:
        limiter.count += 1
    else:
        limiter = PraiseLimiter(sender_id=sender_id, recipient_id=recipient_id, period=period, count=1)
        db.add(limiter)
    db.commit()
    db.refresh(limiter)
    return limiter

def create_praise(db: Session, *, praise_in: PraiseCreate, sender_id: int, strengths: list[Strength]) -> Praise:
    anonymous_name = random.choice(ANONYMOUS_ANIMALS)
    # Note: sender_id is intentionally not saved in the Praise model to ensure anonymity
    db_praise = Praise(
        recipient_id=praise_in.recipient_id,
        message=praise_in.message,
        anonymous_name=anonymous_name,
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
