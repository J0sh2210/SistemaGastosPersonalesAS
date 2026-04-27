from sqlalchemy import Column, Integer, String, DECIMAL, Date, Boolean, ForeignKey, DateTime, func
from database import Base

class Cliente(Base):
    __tablename__ = "Cliente"
    __table_args__ = {'extend_existing': True}

    IdCliente = Column(Integer, primary_key=True, index=True)
    PrimerNombre = Column(String)
    SegundoNombre = Column(String, nullable=True)
    PrimerApellido = Column(String)
    SegundoApellido = Column(String, nullable=True)
    FechaCreacion = Column(DateTime, default=func.now())
    Estado = Column(String(1))

class GastoRecurrente(Base):
    __tablename__ = "GastoRecurrente"
    __table_args__ = {'extend_existing': True}

    IdGastoRecurrente = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String(100), nullable=False)
    Monto = Column(DECIMAL(12, 2), nullable=False)
    FechaInicio = Column(Date, nullable=False)
    Frecuencia = Column(String(20), nullable=False)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"), nullable=False)
    Activo = Column(Boolean, nullable=False, default=True)