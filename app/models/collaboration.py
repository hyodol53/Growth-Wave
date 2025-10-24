from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class InteractionType(str, enum.Enum):
    JIRA_COMMENT = "jira_comment"
    JIRA_MENTION = "jira_mention"
    BITBUCKET_PR_REVIEW = "bitbucket_pr_review"
    BITBUCKET_PR_COMMENT = "bitbucket_pr_comment"

class CollaborationInteraction(Base):
    __tablename__ = "collaboration_interaction"

    id = Column(Integer, primary_key=True, index=True)
    source_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    interaction_type = Column(SAEnum(InteractionType), nullable=False)
    occurred_at = Column(DateTime, nullable=False)

    source_user = relationship("User", foreign_keys=[source_user_id])
    target_user = relationship("User", foreign_keys=[target_user_id])
    project = relationship("Project")
