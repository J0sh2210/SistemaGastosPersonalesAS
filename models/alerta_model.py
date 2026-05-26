from pydantic import BaseModel
from typing import Optional


class AlertaCreate(BaseModel):
    id_usuario: int
    id_categoria: int
    tipo_alerta: str
    mensaje: str
    gastado: float
    limite_presupuesto: float
    porcentaje: float
    mes: int
    anio: int


class AlertaUpdate(BaseModel):
    tipo_alerta: Optional[str] = None
    mensaje: Optional[str] = None
    gastado: Optional[float] = None
    limite_presupuesto: Optional[float] = None
    porcentaje: Optional[float] = None
    mes: Optional[int] = None
    anio: Optional[int] = None


class AlertaResponse(BaseModel):
    id_alerta: int
    id_usuario: int
    id_categoria: int
    tipo_alerta: str
    mensaje: str
    gastado: float
    limite_presupuesto: float
    porcentaje: float
    mes: int
    anio: int