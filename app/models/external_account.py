import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from app.core.database import Base

class AccountType(str, enum.Enum):
    JIRA = "jira"
    GITHUB = "github"
    BITBUCKET = "bitbucket"

class ExternalAccount(Base):
    __tablename__ = "external_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_type = Column(SQLAlchemyEnum(AccountType), nullable=False)
    username = Column(String, nullable=False)
    encrypted_access_token = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="external_accounts")