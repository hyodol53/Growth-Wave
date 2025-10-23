from sqlalchemy.orm import Session
from app.models.strength import Strength

def get_or_create_strengths_by_hashtags(db: Session, hashtags: list[str]) -> list[Strength]:
    strengths = []
    for hashtag in set(h.strip() for h in hashtags if h.strip()): # Use set to avoid duplicate processing
        db_strength = db.query(Strength).filter(Strength.hashtag == hashtag).first()
        if not db_strength:
            db_strength = Strength(hashtag=hashtag)
            db.add(db_strength)
            db.commit()
            db.refresh(db_strength)
        strengths.append(db_strength)
    return strengths
