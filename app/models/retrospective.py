from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base

class Retrospective(Base):
    __tablename__ = "retrospectives"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    evaluation_period_id = Column(Integer, ForeignKey("evaluation_periods.id"), nullable=True)
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User")
    evaluation_period = relationship("EvaluationPeriod")
