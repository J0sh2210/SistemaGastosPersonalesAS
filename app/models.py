from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, DECIMAL, ForeignKey, Integer, String

from database.config import Base

# =============================
# MODELOS SQL
# =============================

class Cliente(Base):
    """Modelo de Cliente"""
    __tablename__ = "Cliente"

    IdCliente = Column(Integer, primary_key=True, index=True)
    PrimerNombre = Column(String(100), nullable=False)
    SegundoNombre = Column(String(100), nullable=True)
    PrimerApellido = Column(String(100), nullable=False)
    SegundoApellido = Column(String(100), nullable=True)
    FechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    Estado = Column(String(1), nullable=False, default="A")


class RecurringExpense(Base):
    """Modelo de Gasto Recurrente"""
    __tablename__ = "GastoRecurrente"

    IdGastoRecurrente = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String(100), nullable=False)
    Monto = Column(DECIMAL(12, 2), nullable=False)
    FechaInicio = Column(Date, nullable=False)
    Frecuencia = Column(String(20), nullable=False)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"), nullable=False)
    is_active = Column("Activo", Boolean, nullable=False, default=True)
