from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    problems = relationship("Problem", back_populates="owner")

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True, index=True)
    problem_text = Column(Text, nullable=False)
    known_answer = Column(Text, nullable=False)
    status = Column(String(50), default='Pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="problems")