from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

praise_strength_association = Table(
    "praise_strength_association",
    Base.metadata,
    Column("praise_id", Integer, ForeignKey("praise.id")),
    Column("strength_id", Integer, ForeignKey("strength.id")),
)


class Strength(Base):
    __tablename__ = "strength"

    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(String, unique=True, index=True, nullable=False)

    praises = relationship(
        "Praise", secondary=praise_strength_association, back_populates="strengths"
    )
