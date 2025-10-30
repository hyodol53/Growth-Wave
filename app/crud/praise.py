from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app import models, schemas
from app.crud.base import CRUDBase
from app.exceptions import PraiseLimitExceeded, InvalidHashtag
from app.utils.anonymous_names import get_anonymous_name_for_praise

class CRUDPraise(CRUDBase[models.Praise, schemas.PraiseCreate, None]):
    def create_with_sender(
        self, 
        db: Session, 
        *, 
        obj_in: schemas.PraiseCreate, 
        sender_id: int,
        current_period_id: int,
        limit: int,
        available_hashtags: list[str]
    ) -> models.Praise:
        # 1. Validate hashtag
        if obj_in.hashtag not in available_hashtags:
            raise InvalidHashtag()

        # 2. Check praise limit
        praise_count = db.query(func.count(self.model.id)).filter(
            and_(
                self.model.sender_id == sender_id,
                self.model.recipient_id == obj_in.recipient_id,
                self.model.evaluation_period_id == current_period_id
            )
        ).scalar()

        if praise_count >= limit:
            raise PraiseLimitExceeded()

        # 3. Create Praise record
        db_obj = self.model(
            **obj_in.model_dump(),
            sender_id=sender_id,
            evaluation_period_id=current_period_id
        )
        db.add(db_obj)

        # 4. Upsert StrengthProfile
        strength_profile = db.query(models.StrengthProfile).filter(
            and_(
                models.StrengthProfile.user_id == obj_in.recipient_id,
                models.StrengthProfile.hashtag == obj_in.hashtag,
                models.StrengthProfile.evaluation_period_id == current_period_id
            )
        ).first()

        if strength_profile:
            strength_profile.count += 1
        else:
            strength_profile = models.StrengthProfile(
                user_id=obj_in.recipient_id,
                hashtag=obj_in.hashtag,
                evaluation_period_id=current_period_id,
                count=1
            )
            db.add(strength_profile)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_inbox_for_user(
        self, 
        db: Session, 
        *, 
        user_id: int,
        anonymous_adjectives: list[str],
        anonymous_animals: list[str]
    ) -> list[schemas.Praise]:
        praises = db.query(self.model).filter(self.model.recipient_id == user_id).order_by(self.model.created_at.desc(), self.model.id.desc()).all()
        
        inbox_items = []
        for p in praises:
            display_name = get_anonymous_name_for_praise(
                praise_id=p.id,
                adjective_list=anonymous_adjectives,
                animal_list=anonymous_animals
            )
            inbox_items.append(
                schemas.Praise(
                    sender_display_name=display_name,
                    message=p.message,
                    hashtag=p.hashtag,
                    created_at=p.created_at
                )
            )
        return inbox_items

    def get_strength_profile(
        self,
        db: Session,
        *,
        user_id: int,
        current_period_id: int
    ) -> list[schemas.StrengthStat]:
        
        strengths = db.query(models.StrengthProfile).filter(
            and_(
                models.StrengthProfile.user_id == user_id,
                models.StrengthProfile.evaluation_period_id == current_period_id
            )
        ).order_by(models.StrengthProfile.count.desc(), models.StrengthProfile.hashtag.asc()).all()

        return [schemas.StrengthStat(hashtag=s.hashtag, count=s.count) for s in strengths]


praise = CRUDPraise(models.Praise)