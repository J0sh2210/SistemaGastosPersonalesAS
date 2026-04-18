from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class Cliente(Base):
    __tablename__ = "Cliente"

    IdCliente = Column(Integer, primary_key=True, index=True)
    PrimerNombre = Column(String)
    SegundoNombre = Column(String, nullable=True)
    PrimerApellido = Column(String)
    SegundoApellido = Column(String, nullable=True)
    FechaCreacion = Column(DateTime, default=func.now())  
    Estado = Column(String(1))


class Usuario(Base):
    __tablename__ = "CuentaUsuario"

    IdCuentaUsuario = Column(Integer, primary_key=True, index=True)
    NombreUsuario = Column(String, unique=True)
    Contraseña = Column(String)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"))