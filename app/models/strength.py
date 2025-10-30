from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class StrengthProfile(Base):
    __tablename__ = "strength_profile"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    hashtag = Column(String, primary_key=True)
    evaluation_period_id = Column(Integer, ForeignKey("evaluation_periods.id"), primary_key=True)
    
    count = Column(Integer, nullable=False, default=0)

    user = relationship("User")
    evaluation_period = relationship("EvaluationPeriod")
