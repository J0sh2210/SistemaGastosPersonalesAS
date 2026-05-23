from typing import Optional
from pydantic import BaseModel


class PresupuestoCreate(BaseModel):
    monto_presupuesto: float
    id_categoria: Optional[int] = None
    mes_aplicacion: str
    id_usuario: int


class PresupuestoUpdate(BaseModel):
    monto_presupuesto: Optional[float] = None
    id_categoria: Optional[int] = None
    mes_aplicacion: Optional[str] = None
    id_usuario: Optional[int] = None


class PresupuestoResponse(BaseModel):
    id_presupuesto: int
    monto_presupuesto: float
    id_categoria: Optional[int]
    mes_aplicacion: str
    id_usuario: int

