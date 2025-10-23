from unittest.mock import MagicMock
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate
from app.models.user import User, UserRole

def test_create_user_returns_object():
    """
    Tests that the create_user CRUD function returns the created object.
    """
    # Arrange
    mock_db = MagicMock()
    user_in = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password",
        role=UserRole.EMPLOYEE
    )

    # Act
    result = crud_user.create(db=mock_db, obj_in=user_in)

    # Assert
    assert result is not None
    assert isinstance(result, User)
    assert result.username == user_in.username
    assert result.email == user_in.email
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
