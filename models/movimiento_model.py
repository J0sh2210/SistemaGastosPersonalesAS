from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from database import Base


class Movimiento(Base):
    __tablename__ = "Movimiento"

    IdMovimiento = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String)
    Monto = Column(DECIMAL(12, 2))
    FechaMovimiento = Column(DateTime)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"))
    IdTipo = Column(Integer, ForeignKey("TipoMovimiento.IdTipo"))