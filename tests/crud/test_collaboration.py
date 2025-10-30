from sqlalchemy.orm import Session
from datetime import datetime

from app import crud
from app.models.collaboration import InteractionType, CollaborationCategory
from app.schemas.collaboration import CollaborationInteractionCreate
from tests.utils.user import create_random_user
from tests.utils.project import create_random_project

def test_create_collaboration_interaction(db: Session) -> None:
    """
    Test creating a collaboration interaction with a category.
    """
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    pm = create_random_user(db)
    project = create_random_project(db, pm_id=pm.id)
    
    interaction_in = CollaborationInteractionCreate(
        source_user_id=user1.id,
        target_user_id=user2.id,
        project_id=project.id,
        interaction_type=InteractionType.JIRA_COMMENT,
        category=CollaborationCategory.SUPPORT,
        occurred_at=datetime.utcnow()
    )
    
    interaction = crud.collaboration.collaboration_interaction.create(db, obj_in=interaction_in)
    
    assert interaction.source_user_id == user1.id
    assert interaction.target_user_id == user2.id
    assert interaction.project_id == project.id
    assert interaction.interaction_type == InteractionType.JIRA_COMMENT
    assert interaction.category == CollaborationCategory.SUPPORT

def test_get_collaboration_data_analysis(db: Session) -> None:
    """
    Test the analysis part of get_collaboration_data with categories.
    """
    user1 = create_random_user(db, full_name="Supporter Sam")
    user2 = create_random_user(db, full_name="Requester Rick")
    user3 = create_random_user(db, full_name="Normal Nick")
    pm = create_random_user(db)
    project = create_random_project(db, pm_id=pm.id)

    # Create some interactions
    # User1 supports User2 twice
    crud.collaboration.collaboration_interaction.create(db, obj_in=CollaborationInteractionCreate(
        source_user_id=user1.id, target_user_id=user2.id, project_id=project.id,
        interaction_type=InteractionType.JIRA_COMMENT, category=CollaborationCategory.SUPPORT, occurred_at=datetime.utcnow()
    ))
    crud.collaboration.collaboration_interaction.create(db, obj_in=CollaborationInteractionCreate(
        source_user_id=user1.id, target_user_id=user3.id, project_id=project.id,
        interaction_type=InteractionType.BITBUCKET_PR_REVIEW, category=CollaborationCategory.SUPPORT, occurred_at=datetime.utcnow()
    ))
    
    # User2 requests from User1 once
    crud.collaboration.collaboration_interaction.create(db, obj_in=CollaborationInteractionCreate(
        source_user_id=user2.id, target_user_id=user1.id, project_id=project.id,
        interaction_type=InteractionType.JIRA_MENTION, category=CollaborationCategory.REQUEST, occurred_at=datetime.utcnow()
    ))

    # Get collaboration data for the project
    collab_data = crud.collaboration.collaboration_interaction.get_collaboration_data(db, project_id=project.id)

    # Check the analysis
    analysis = collab_data.analysis
    
    assert len(analysis.most_support) == 1
    assert analysis.most_support[0]["user_id"] == user1.id
    assert analysis.most_support[0]["full_name"] == "Supporter Sam"
    assert analysis.most_support[0]["count"] == 2

    assert len(analysis.most_requests) == 1
    assert analysis.most_requests[0]["user_id"] == user2.id
    assert analysis.most_requests[0]["full_name"] == "Requester Rick"
    assert analysis.most_requests[0]["count"] == 1
