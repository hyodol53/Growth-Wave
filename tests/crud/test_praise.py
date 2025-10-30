from sqlalchemy.orm import Session
import pytest

from app import crud, models
from app.schemas.praise import PraiseCreate
from app.exceptions import PraiseLimitExceeded, InvalidHashtag
from app.core.config import settings
from app.utils.anonymous_names import get_anonymous_name_for_praise
from tests.utils.user import create_random_user
from tests.utils.evaluation import create_random_evaluation_period

def test_create_praise(db: Session) -> None:
    """
    Test creating a praise successfully.
    """
    sender = create_random_user(db)
    recipient = create_random_user(db)
    active_period = create_random_evaluation_period(db, is_active=True)
    
    praise_in = PraiseCreate(recipient_id=recipient.id, message="Test message", hashtag="#해결사")
    
    praise = crud.praise.create_with_sender(
        db=db,
        obj_in=praise_in,
        sender_id=sender.id,
        current_period_id=active_period.id,
        limit=settings.PRAISE_LIMIT_PER_PERIOD,
        available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
    )
    
    assert praise.sender_id == sender.id
    assert praise.recipient_id == recipient.id
    assert praise.message == "Test message"
    assert praise.hashtag == "#해결사"
    
    # Check strength profile
    profile = crud.praise.get_strength_profile(db, user_id=recipient.id, current_period_id=active_period.id)
    assert len(profile) == 1
    assert profile[0].hashtag == "#해결사"
    assert profile[0].count == 1

def test_praise_limit(db: Session) -> None:
    """
    Test that praising is limited.
    """
    sender = create_random_user(db)
    recipient = create_random_user(db)
    active_period = create_random_evaluation_period(db, is_active=True)
    limit = 2 # Use a small limit for testing
    
    praise_in = PraiseCreate(recipient_id=recipient.id, message="Test", hashtag="#소통왕")
    
    # Praise up to the limit
    for _ in range(limit):
        crud.praise.create_with_sender(
            db=db, obj_in=praise_in, sender_id=sender.id, current_period_id=active_period.id,
            limit=limit, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
        )
        
    # The next one should fail
    with pytest.raises(PraiseLimitExceeded):
        crud.praise.create_with_sender(
            db=db, obj_in=praise_in, sender_id=sender.id, current_period_id=active_period.id,
            limit=limit, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
        )

def test_invalid_hashtag(db: Session) -> None:
    """
    Test that using an invalid hashtag raises an error.
    """
    sender = create_random_user(db)
    recipient = create_random_user(db)
    active_period = create_random_evaluation_period(db, is_active=True)
    
    praise_in = PraiseCreate(recipient_id=recipient.id, message="Test", hashtag="#없는태그")
    
    with pytest.raises(InvalidHashtag):
        crud.praise.create_with_sender(
            db=db, obj_in=praise_in, sender_id=sender.id, current_period_id=active_period.id,
            limit=settings.PRAISE_LIMIT_PER_PERIOD, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
        )

def test_get_inbox_for_user(db: Session) -> None:
    """
    Test retrieving a user's praise inbox.
    """
    sender1 = create_random_user(db)
    sender2 = create_random_user(db)
    recipient = create_random_user(db)
    active_period = create_random_evaluation_period(db, is_active=True)
    
    praise_in1 = PraiseCreate(recipient_id=recipient.id, message="First praise", hashtag="#협업왕")
    praise1 = crud.praise.create_with_sender(
        db, obj_in=praise_in1, sender_id=sender1.id, current_period_id=active_period.id,
        limit=5, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
    )
    
    praise_in2 = PraiseCreate(recipient_id=recipient.id, message="Second praise", hashtag="#디테일장인")
    praise2 = crud.praise.create_with_sender(
        db, obj_in=praise_in2, sender_id=sender2.id, current_period_id=active_period.id,
        limit=5, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS
    )
    
    inbox = crud.praise.get_inbox_for_user(
        db, user_id=recipient.id, 
        anonymous_adjectives=settings.PRAISE_ANONYMOUS_ADJECTIVES,
        anonymous_animals=settings.PRAISE_ANONYMOUS_ANIMALS
    )
    
    assert len(inbox) == 2
    # The order is descending by creation time
    assert inbox[0].message == "Second praise"
    assert inbox[1].message == "First praise"
    
    # Check anonymous name generation
    name1 = get_anonymous_name_for_praise(praise1.id, settings.PRAISE_ANONYMOUS_ADJECTIVES, settings.PRAISE_ANONYMOUS_ANIMALS)
    name2 = get_anonymous_name_for_praise(praise2.id, settings.PRAISE_ANONYMOUS_ADJECTIVES, settings.PRAISE_ANONYMOUS_ANIMALS)
    
    # The inbox is sorted desc, so praise2 comes first
    assert inbox[0].sender_display_name == name2
    assert inbox[1].sender_display_name == name1

def test_get_strength_profile(db: Session) -> None:
    """
    Test aggregating and retrieving a strength profile.
    """
    sender = create_random_user(db)
    recipient = create_random_user(db)
    active_period = create_random_evaluation_period(db, is_active=True)
    
    # Send multiple praises
    crud.praise.create_with_sender(db, obj_in=PraiseCreate(recipient_id=recipient.id, message="m1", hashtag="#해결사"), sender_id=sender.id, current_period_id=active_period.id, limit=5, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS)
    crud.praise.create_with_sender(db, obj_in=PraiseCreate(recipient_id=recipient.id, message="m2", hashtag="#소통왕"), sender_id=sender.id, current_period_id=active_period.id, limit=5, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS)
    crud.praise.create_with_sender(db, obj_in=PraiseCreate(recipient_id=recipient.id, message="m3", hashtag="#해결사"), sender_id=sender.id, current_period_id=active_period.id, limit=5, available_hashtags=settings.PRAISE_AVAILABLE_HASHTAGS)
    
    profile = crud.praise.get_strength_profile(db, user_id=recipient.id, current_period_id=active_period.id)
    
    assert len(profile) == 2
    # Should be sorted by count desc, then hashtag asc
    assert profile[0].hashtag == "#해결사"
    assert profile[0].count == 2
    assert profile[1].hashtag == "#소통왕"
    assert profile[1].count == 1
