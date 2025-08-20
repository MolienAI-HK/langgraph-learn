from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_completed = Column(Boolean, default=False)

class FoodAnalysis(Base):
    __tablename__ = "food_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    image_path = Column(String)
    calories = Column(Float)
    is_dieting = Column(Boolean, nullable=True)
    recommendation = Column(String)
    comparison_table = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)