from pydantic import BaseModel, Field, PositiveFloat, ConfigDict
from datetime import datetime
from typing import Optional
from datetime import date
from enum import Enum

# Clase base con lo que comparten creación y edición
class IngresoBase(BaseModel):
    Concepto: str = Field(..., min_length=1, max_length=30)
    Monto: float = Field(..., gt=0)

# Al crear un ingreso, necesitamos saber de qué cliente es
class IngresoCreate(IngresoBase):
    IdCliente: int
    IdMovimiento: int
    IdCategoria: int
    IdMeta: Optional[int] = None
    IdTipo: int

# Al editar, solo recibimos concepto y monto (heredados de IngresoBase)
class IngresoUpdate(IngresoBase):
    IdCategoria: int
    pass

# Lo que la API le responde al Frontend
class IngresoResponse(IngresoBase):
    IdMovimiento: int
    FechaMovimiento: datetime
    IdCliente: int
    IdTipo: int
    IdCategoria: Optional[int] = None
    IdMeta: Optional[int] = None

class MovimientoMesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    IdMovimiento: int
    Concepto: str
    Monto: float
    FechaMovimiento: datetime
    IdCliente: int
    IdTipo: int
    NombreTipoMovimiento: str  # Devolverá "Ingreso" o "Egreso"

class GastoBase(BaseModel):
    Concepto: str = Field(..., min_length=1, max_length=30)
    Monto: float = Field(..., gt=0)
    IdCliente: int
    IdCategoria: Optional[int] = None

class GastoCreate(GastoBase):
    pass

class GastoResponse(GastoBase):
    model_config = ConfigDict(from_attributes=True)
    
    IdMovimiento: int
    FechaMovimiento: datetime

class FrecuenciaEnum(str, Enum):
    mensual = "mensual"

class CrearGastoRecurrente(BaseModel):
    Concepto: str = Field(..., min_length=1)
    Monto: PositiveFloat
    FechaInicio: date
    Frecuencia: FrecuenciaEnum
    IdCliente: int

class LeerGastoRecurrente(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    IdGastoRecurrente: int
    Concepto: str
    Monto: float
    FechaInicio: date
    Frecuencia: str
    IdCliente: int
    Activo: bool

class ActualizarGastoRecurrente(BaseModel):
    Concepto: Optional[str] = None
    Monto: Optional[PositiveFloat] = None
    Frecuencia: Optional[FrecuenciaEnum] = None

class PresupuestoBase(BaseModel):
    IdCliente: int = Field(..., gt=0)
    Anio: int
    Mes: int = Field(..., ge=1, le=12)
    MontoPresupuestado: PositiveFloat = Field(..., gt=0)

class PresupuestoCreate(PresupuestoBase):
    pass

class PresupuestoUpdate(PresupuestoBase):
    pass

class PresupuestoResponse(PresupuestoBase):
    model_config = ConfigDict(from_attributes=True)
    
    IdPresupuesto: int
    FechaCreacion: datetime

from typing import List
from pydantic import BaseModel
from datetime import datetime

class ResumenMesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    anio: int
    mes: int
    idCliente: int
    totalIngresos: float
    totalEgresos: float
    balance: float
    ingresos: List[dict]
    egresos: List[dict]
