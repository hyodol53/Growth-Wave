from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class PraiseLimiter(Base):
    __tablename__ = "praise_limiter"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    period = Column(String, nullable=False, index=True) # e.g., "2024-H1"
    count = Column(Integer, nullable=False, default=0)
    anonymous_name = Column(String, nullable=True) # Can be null for records created before this feature

    sender = relationship("User", back_populates="praises_sent_log", foreign_keys=[sender_id])
    recipient = relationship("User", back_populates="praises_received_log", foreign_keys=[recipient_id])
