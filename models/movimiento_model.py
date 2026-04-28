from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from database import Base
from pydantic import BaseModel


class Movimiento(Base):
    __tablename__ = "Movimiento"

    IdMovimiento = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String)
    Monto = Column(DECIMAL(12, 2))
    FechaMovimiento = Column(DateTime)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"))
    IdTipo = Column(Integer, ForeignKey("TipoMovimiento.IdTipo"))

class EditarCategoriaRequest(BaseModel):
    idCategoria: int


class EditarCategoriaResponse(BaseModel):
    message: str

class DiferenciaResponse(BaseModel):
    total: float
