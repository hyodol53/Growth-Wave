import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from app.core.database import Base

class Provider(str, enum.Enum):
    JIRA = "jira"
    BITBUCKET = "bitbucket"

class ExternalAccount(Base):
    __tablename__ = "external_accounts"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(SQLAlchemyEnum(Provider), nullable=False)
    account_id = Column(String, nullable=False) # User's email or username in the external service
    encrypted_credentials = Column(String, nullable=False) # Encrypted API token, OAuth token, etc.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="external_accounts")