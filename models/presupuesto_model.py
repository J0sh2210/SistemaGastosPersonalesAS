from sqlalchemy import Column, Integer, SmallInteger, DECIMAL, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo SQLAlchemy
class PresupuestoMensual(Base):
    __tablename__ = "PresupuestoMensual"
    IdPresupuesto = Column(Integer, primary_key=True, index=True)
    IdCliente = Column(Integer, nullable=False)
    Anio = Column(SmallInteger, nullable=False)
    Mes = Column(SmallInteger, nullable=False)
    MontoLimite = Column(DECIMAL(12,2), nullable=False)
    FechaCreacion = Column(DateTime, server_default=func.now())

# Pydantic Schemas para API
class PresupuestoCreate(BaseModel):
    IdCliente: int
    Anio: int
    Mes: int
    MontoLimite: float

class PresupuestoUpdate(BaseModel):
    MontoLimite: Optional[float] = None

class PresupuestoResponse(BaseModel):
    IdPresupuesto: int
    IdCliente: int
    Anio: int
    Mes: int
    MontoLimite: float
    FechaCreacion: datetime

    class Config:
        from_attributes = True

