import pytest
from sqlalchemy.orm import RelationshipProperty
from app import models, schemas

def test_schema_imports():
    """
    Tests that all Pydantic schemas can be imported from the top-level package.
    """
    assert hasattr(schemas, "User")
    assert hasattr(schemas, "UserCreate")
    assert hasattr(schemas, "Organization")
    assert hasattr(schemas, "Token")
    assert hasattr(schemas, "ExternalAccount")

def test_model_imports():
    """
    Tests that all SQLAlchemy models can be imported from the top-level package.
    """
    assert hasattr(models, "User")
    assert hasattr(models, "Organization")
    assert hasattr(models, "ExternalAccount")

def test_model_relationships():
    """
    Inspects all SQLAlchemy model relationships and ensures they point to valid,
    existing classes. This prevents errors from undefined model relationships.
    """
    all_models = [models.User, models.Organization, models.ExternalAccount]
    for model in all_models:
        for prop in model.__mapper__.iterate_properties:
            if isinstance(prop, RelationshipProperty):
                # This access will raise an error if the related class is not found
                try:
                    related_class = prop.mapper.class_
                    print(f"Successfully resolved relationship '{model.__name__}.{prop.key}' -> '{related_class.__name__}'")
                except Exception as e:
                    pytest.fail(
                        f"Failed to resolve relationship '{model.__name__}.{prop.key}'. "
                        f"Ensure the related model is correctly defined and imported. Error: {e}"
                    )
