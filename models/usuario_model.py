from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from database import Base


# --- MODELOS SQLALCHEMY ---

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


# --- SCHEMAS PYDANTIC ---

class RegistroUsuario(BaseModel):
    username: str
    password: str
    primerNombre: str
    segundoNombre: str | None = None
    primerApellido: str
    segundoApellido: str | None = None


class LoginUsuario(BaseModel):
    username: str
    password: str
