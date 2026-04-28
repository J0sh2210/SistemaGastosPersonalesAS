from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GastoBase(BaseModel):
    Concepto: str = Field(..., min_length=1, max_length=30)
    Monto: float = Field(..., gt=0)
    IdCliente: int
    IdCategoria: Optional[int] = None

class GastoCreate(GastoBase):
    pass

class GastoResponse(GastoBase):
    IdMovimiento: int
    FechaMovimiento: datetime

    class Config:
        from_attributes = True # Equivalente a orm_mode en Pydantic v2