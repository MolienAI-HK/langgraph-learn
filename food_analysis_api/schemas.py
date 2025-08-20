from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SessionBase(BaseModel):
    session_id: str

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    created_at: datetime
    is_completed: bool
    
    class Config:
        orm_mode = True

class DietResponse(BaseModel):
    is_dieting: bool

class AnalysisBase(BaseModel):
    session_id: str
    image_path: Optional[str] = None
    calories: Optional[float] = None
    is_dieting: Optional[bool] = None

class AnalysisCreate(AnalysisBase):
    pass

class Analysis(AnalysisBase):
    id: int
    recommendation: Optional[str] = None
    comparison_table: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class HistoryResponse(BaseModel):
    session_id: str
    analyses: List[Analysis]
    created_at: datetime
    is_completed: bool