from datetime import date
from sqlalchemy import Boolean, Column, Date, DECIMAL, ForeignKey, Integer, String

from app.database import Base
#/*ELR_ENMA*/


# =============================
# MODELOS SQL
# =============================
class Cliente(Base):
    __tablename__ = "Cliente"

    IdCliente = Column(Integer, primary_key=True, index=True)
    PrimerNombre = Column(String(100), nullable=False)
    SegundoNombre = Column(String(100), nullable=True)
    PrimerApellido = Column(String(100), nullable=False)
    SegundoApellido = Column(String(100), nullable=True)
    FechaCreacion = Column(Date, nullable=False, default=date.today)
    Estado = Column(String(1), nullable=False, default="A")


class RecurringExpense(Base):
    __tablename__ = "GastoRecurrente"

    IdGastoRecurrente = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String(100), nullable=False)
    Monto = Column(DECIMAL(12, 2), nullable=False)
    FechaInicio = Column(Date, nullable=False)
    Frecuencia = Column(String(20), nullable=False)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"), nullable=False)
    is_active = Column("Activo", Boolean, nullable=False, default=True)
