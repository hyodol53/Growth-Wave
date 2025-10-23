from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.api import deps
from app.exceptions import PraiseLimitExceeded

router = APIRouter()

@router.post("/", response_model=schemas.Praise, status_code=status.HTTP_201_CREATED)
def create_praise(
    *,
    db: Session = Depends(deps.get_db),
    praise_in: schemas.PraiseCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new praise for another user.

    - A user cannot praise themselves.
    - The number of praises to a specific user is limited.
    """
    if praise_in.recipient_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot praise yourself.",
        )

    recipient = crud.user.user.get(db, id=praise_in.recipient_id)
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found.",
        )

    # Get or create strength hashtags
    strengths = crud.strength.get_or_create_strengths_by_hashtags(db, hashtags=praise_in.hashtags)

    try:
        created_praise = crud.praise.create_praise(
            db, praise_in=praise_in, sender_id=current_user.id, strengths=strengths
        )
    except PraiseLimitExceeded:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"You can only praise this user {crud.praise.PRAISE_LIMIT_PER_PERIOD} times per period.",
        )

    return created_praise


@router.get("/inbox/", response_model=List[schemas.Praise])
def read_praise_inbox(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve the current user's praise inbox, sorted by most recent.
    """
    praises = crud.praise.get_praises_for_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return praises


@router.get("/users/{user_id}/strength-profile/", response_model=schemas.StrengthProfile)
def read_user_strength_profile(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve a user's public strength profile, which consists of aggregated hashtag counts.
    """
    user = crud.user.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    strength_stats = crud.praise.get_strength_profile_for_user(db, user=user)

    return schemas.StrengthProfile(
        user_id=user.id,
        full_name=user.full_name,
        strengths=strength_stats
    )