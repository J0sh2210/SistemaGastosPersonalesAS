from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Boolean
from database import Base

class GastoRecurrente(Base):
    __tablename__ = "GastoRecurrente"

    IdGastoRecurrente = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String(100), nullable=False)
    Monto = Column(DECIMAL(12,2), nullable=False)
    FechaInicio = Column(DateTime, nullable=False)
    Frecuencia = Column(String(20), nullable=False)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"), nullable=False)
    Activo = Column(Boolean, default=True)