from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.services import retrospective_generator

router = APIRouter()

@router.post("/generate", response_model=schemas.retrospective.RetrospectiveUpdate)
def generate_draft(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Generate a new retrospective draft for the current user using AI.
    This does NOT save the retrospective to the database.
    """
    try:
        draft_content = retrospective_generator.generate_retrospective_draft(db=db, user=current_user)
        return {"content": draft_content}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to generate draft: {e}")

@router.post("", response_model=schemas.Retrospective, status_code=status.HTTP_201_CREATED)
def create_retrospective(
    *,
    db: Session = Depends(deps.get_db),
    retrospective_in: schemas.RetrospectiveCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new retrospective for the current user.
    """
    retrospective = crud.retrospective.create_with_owner(
        db=db, obj_in=retrospective_in, user_id=current_user.id
    )
    return retrospective

@router.get("", response_model=List[schemas.Retrospective])
def read_retrospectives(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve retrospectives for the current user.
    """
    return crud.retrospective.get_multi_by_owner(db=db, user_id=current_user.id)

@router.get("/{id}", response_model=schemas.Retrospective)
def read_retrospective(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a specific retrospective by ID, owned by the current user.
    """
    retrospective = crud.retrospective.get_by_owner(db=db, id=id, user_id=current_user.id)
    if not retrospective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Retrospective not found")
    return retrospective

@router.put("/{id}", response_model=schemas.Retrospective)
def update_retrospective(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    retrospective_in: schemas.RetrospectiveUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a retrospective owned by the current user.
    """
    retrospective = crud.retrospective.get_by_owner(db=db, id=id, user_id=current_user.id)
    if not retrospective:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Retrospective not found")
    retrospective = crud.retrospective.update(db=db, db_obj=retrospective, obj_in=retrospective_in)
    return retrospective

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_retrospective(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> None:
    """
    Delete a retrospective owned by the current user.
    """
    result = crud.retrospective.remove_by_owner(db=db, id=id, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Retrospective not found")
    return None