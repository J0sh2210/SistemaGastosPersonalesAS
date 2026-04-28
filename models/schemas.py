from pydantic import BaseModel, Field, PositiveFloat
from datetime import datetime
from typing import Optional

from datetime import date
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from datetime import datetime

# Clase base con lo que comparten creación y edición
class IngresoBase(BaseModel):
    Concepto: str = Field(..., min_length=1, max_length=30)
    Monto: float = Field(..., gt=0)

# Al crear un ingreso, necesitamos saber de qué cliente es
class IngresoCreate(IngresoBase):
    IdCliente: int

# Al editar, solo recibimos concepto y monto (heredados de IngresoBase)
class IngresoUpdate(IngresoBase):
    pass

# Lo que la API le responde al Frontend
class IngresoResponse(IngresoBase):
    IdMovimiento: int
    FechaMovimiento: datetime
    IdCliente: int
    IdTipo: int
class MovimientoMesResponse(BaseModel):
    IdMovimiento: int
    Concepto: str
    Monto: float
    FechaMovimiento: datetime
    IdCliente: int
    IdTipo: int
    NombreTipoMovimiento: str  # Devolverá "Ingreso" o "Egreso"

    class Config:
        from_attributes = True

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