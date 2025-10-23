from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.strength import praise_strength_association


class Praise(Base):
    __tablename__ = "praise"

    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(String, nullable=False)
    anonymous_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipient = relationship("User", back_populates="praises_received")
    strengths = relationship(
        "Strength", secondary=praise_strength_association, back_populates="praises"
    )
