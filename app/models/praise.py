from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Praise(Base):
    __tablename__ = "praise"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    evaluation_period_id = Column(Integer, ForeignKey("evaluation_periods.id"), nullable=False, index=True)
    
    message = Column(Text, nullable=False)
    hashtag = Column(String, nullable=False) # 선택된 강점 카테고리
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="praises_received")
    evaluation_period = relationship("EvaluationPeriod")
