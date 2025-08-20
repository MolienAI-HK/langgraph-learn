from sqlalchemy.orm import Session
from . import models, schemas
from uuid import uuid4

def create_session(db: Session):
    session_id = str(uuid4())
    db_session = models.UserSession(session_id=session_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: str):
    return db.query(models.UserSession).filter(
        models.UserSession.session_id == session_id
    ).first()

def complete_session(db: Session, session_id: str):
    db_session = get_session(db, session_id)
    if db_session:
        db_session.is_completed = True
        db.commit()
        db.refresh(db_session)
    return db_session

def create_analysis(db: Session, analysis: schemas.AnalysisCreate):
    db_analysis = models.FoodAnalysis(**analysis.dict())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_analyses_by_session(db: Session, session_id: str):
    return db.query(models.FoodAnalysis).filter(
        models.FoodAnalysis.session_id == session_id
    ).all()

def get_all_analyses(db: Session):
    return db.query(models.FoodAnalysis).order_by(
        models.FoodAnalysis.created_at.desc()
    ).all()