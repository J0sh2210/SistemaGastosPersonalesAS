from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Presupuesto(Base):
    __tablename__ = "presupuesto"
    
    IdPresupuesto = Column(Integer, primary_key=True, index=True)
    IdCliente = Column(Integer, nullable=False)
    Anio = Column(Integer, nullable=False)
    Mes = Column(Integer, nullable=False)
    MontoPresupuestado = Column(Float, nullable=False)
    FechaCreacion = Column(DateTime(timezone=True), server_default=func.now())

# NOTA: Tabla 'presupuesto' debe crearse manualmente en BD para funcionalidad completa
