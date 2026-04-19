from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, PositiveFloat

# =============================
# ENUMS
# =============================

class FrecuenciaEnum(str, Enum):
    """Enumeración de frecuencias"""
    mensual = "mensual"


# =============================
# ESQUEMAS PYDANTIC
# =============================

class ClienteCreate(BaseModel):
    """Esquema para crear cliente"""
    PrimerNombre: str = Field(..., min_length=1)
    SegundoNombre: Optional[str] = None
    PrimerApellido: str = Field(..., min_length=1)
    SegundoApellido: Optional[str] = None


class ClienteRead(ClienteCreate):
    """Esquema para leer cliente"""
    IdCliente: int
    FechaCreacion: datetime
    Estado: str

    class Config:
        from_attributes = True


class RecurringExpenseCreate(BaseModel):
    """Esquema para crear gasto recurrente"""
    Concepto: str = Field(..., min_length=1, description="Nombre del gasto")
    Monto: PositiveFloat
    FechaInicio: date
    Frecuencia: FrecuenciaEnum
    IdCliente: int


class RecurringExpenseRead(RecurringExpenseCreate):
    """Esquema para leer gasto recurrente"""
    IdGastoRecurrente: int
    is_active: bool

    class Config:
        from_attributes = True


class RecurringExpenseUpdate(BaseModel):
    """Esquema para actualizar gasto recurrente"""
    Concepto: Optional[str] = Field(None, min_length=1, description="Nombre del gasto")
    Monto: Optional[PositiveFloat] = None
    FechaInicio: Optional[date] = None
    Frecuencia: Optional[FrecuenciaEnum] = None
    IdCliente: Optional[int] = None
    is_active: Optional[bool] = None
