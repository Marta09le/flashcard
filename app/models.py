from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .db import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False)
    translation = Column(String(200), nullable=False)
    example = Column(String(300), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
