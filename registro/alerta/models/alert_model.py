from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertCreate(BaseModel):
    month: str
    category: str
    spent: float
    budgeted: float
    percentage: float
    status: str  # 'warning' or 'exceeded'

class AlertUpdate(BaseModel):
    month: Optional[str] = None
    category: Optional[str] = None
    spent: Optional[float] = None
    budgeted: Optional[float] = None
    percentage: Optional[float] = None
    status: Optional[str] = None

class AlertResponse(BaseModel):
    id: str
    month: str
    category: str
    spent: float
    budgeted: float
    percentage: float
    status: str
    created_at: str

