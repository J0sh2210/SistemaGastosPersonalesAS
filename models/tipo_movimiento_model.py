from sqlalchemy import Column, Integer, String
from database import Base

class TipoMovimiento(Base):
    __tablename__ = "TipoMovimiento"

    IdTipo = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String)
    Naturaleza = Column(String)