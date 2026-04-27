from pydantic import BaseModel, Field, PositiveFloat
from datetime import datetime
from typing import Optional

from datetime import date
from typing import Optional
from enum import Enum

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

class FrecuenciaEnum(str, Enum):
    mensual = "mensual"

class CrearGastoRecurrente(BaseModel):
    Concepto: str = Field(..., min_length=1)
    Monto: PositiveFloat
    FechaInicio: date
    Frecuencia: FrecuenciaEnum
    IdCliente: int

class LeerGastoRecurrente(BaseModel):
    IdGastoRecurrente: int
    Concepto: str
    Monto: float
    FechaInicio: date
    Frecuencia: str
    IdCliente: int
    Activo: bool

    class Config:
        from_attributes = True

class ActualizarGastoRecurrente(BaseModel):
    Concepto: Optional[str] = None
    Monto: Optional[PositiveFloat] = None
    Frecuencia: Optional[FrecuenciaEnum] = None