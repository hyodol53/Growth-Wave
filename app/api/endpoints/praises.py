from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.exceptions import PraiseLimitExceeded, InvalidHashtag
from app.core.config import settings

router = APIRouter()


@router.post("", status_code=201, response_model=schemas.Msg)
def create_praise(
    *,
    db: Session = Depends(deps.get_db),
    praise_in: schemas.PraiseCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new praise.
    """
    if praise_in.recipient_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot praise yourself.")

    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="There is no active evaluation period.")

    try:
        crud.praise.create_with_sender(
            db=db,
            obj_in=praise_in,
            sender_id=current_user.id,
            current_period_id=active_period.id,
            limit=settings.PRAISE_LIMIT_PER_PERIOD,
            available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
        )
    except InvalidHashtag:
        raise HTTPException(status_code=400, detail=f"Invalid hashtag. Available hashtags are: {settings.PRAISE_AVAILABLE_HASHTAGS}")
    except PraiseLimitExceeded:
        raise HTTPException(status_code=400, detail=f"You have already praised this person {settings.PRAISE_LIMIT_PER_PERIOD} times in this period.")
    
    return {"message": "Praise sent successfully"}


@router.get("/inbox", response_model=List[schemas.Praise])
def read_my_praise_inbox(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve praise inbox for the current user.
    """
    inbox = crud.praise.get_inbox_for_user(
        db=db, 
        user_id=current_user.id,
        anonymous_adjectives=settings.PRAISE_ANONYMOUS_ADJECTIVES,
        anonymous_animals=settings.PRAISE_ANONYMOUS_ANIMALS
    )
    return inbox


@router.get("/users/{user_id}/strength-profile", response_model=schemas.StrengthProfile)
def read_user_strength_profile(
    user_id: int,
    *,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a user's public strength profile.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    active_period = crud.evaluation_period.get_active_period(db)
    if not active_period:
        raise HTTPException(status_code=400, detail="There is no active evaluation period.")

    badges = crud.praise.get_strength_profile(
        db=db,
        user_id=user_id,
        current_period_id=active_period.id
    )
    
    return schemas.StrengthProfile(
        user_id=user.id,
        full_name=user.full_name,
        current_period=active_period.name,
        badges=badges
    )
