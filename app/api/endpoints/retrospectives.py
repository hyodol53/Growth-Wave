from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.crud import retrospective_generator

router = APIRouter()


@router.post("/generate", response_model=schemas.RetrospectiveResponse)
def generate_ai_retrospective(
    *,
    db: Session = Depends(deps.get_db),
    retrospective_in: schemas.RetrospectiveCreateRequest,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Generate AI-based retrospective for the current user.
    """
    summary = retrospective_generator.generate_retrospective(
        db, user=current_user, start_date=retrospective_in.start_date, end_date=retrospective_in.end_date
    )
    return schemas.RetrospectiveResponse(content=summary)
