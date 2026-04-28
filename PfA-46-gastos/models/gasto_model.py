from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class GastoCreate(BaseModel):
    concepto: str
    monto: float
    id_cliente: int
    id_categoria: int
    fecha_movimiento: Optional[datetime] = None


class GastoUpdate(BaseModel):
    concepto: Optional[str] = None
    monto: Optional[float] = None
    id_categoria: Optional[int] = None
    fecha_movimiento: Optional[datetime] = None

