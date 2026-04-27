from datetime import date
from typing import Generator, List, Optional
from enum import Enum

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, PositiveFloat
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DECIMAL,
    Date,
    Boolean,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# =====================================
# CONEXIÓN SQL SERVER
# =====================================
URL_BASE_DATOS = (
    "mssql+pyodbc://@ENMITA\\SQLEXPRESS/SistemasGastosAS"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

motor = create_engine(URL_BASE_DATOS, echo=True)
SesionLocal = sessionmaker(bind=motor, autocommit=False, autoflush=False)
Base = declarative_base()

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

# =====================================
# ENUM FRECUENCIA
# =====================================
class FrecuenciaEnum(str, Enum):
    mensual = "mensual"

# =====================================
# TABLA GASTO RECURRENTE
# =====================================
class GastoRecurrente(Base):
    __tablename__ = "GastoRecurrente"

    IdGastoRecurrente = Column(Integer, primary_key=True, index=True)
    Concepto = Column(String(100), nullable=False)
    Monto = Column(DECIMAL(12, 2), nullable=False)
    FechaInicio = Column(Date, nullable=False)
    Frecuencia = Column(String(20), nullable=False)
    IdCliente = Column(Integer, ForeignKey("Cliente.IdCliente"), nullable=False)
    Activo = Column(Boolean, nullable=False, default=True)

Base.metadata.create_all(bind=motor)

# =====================================
# MODELOS PYDANTIC
# =====================================
class CrearGastoRecurrente(BaseModel):
    Concepto: str = Field(..., min_length=1)
    Monto: PositiveFloat
    FechaInicio: date
    Frecuencia: FrecuenciaEnum
    IdCliente: int

class LeerGastoRecurrente(BaseModel):
    IdGastoRecurrente: int
    Concepto: str
    Monto: float
    FechaInicio: date
    Frecuencia: str
    IdCliente: int
    Activo: bool

    class Config:
        orm_mode = True

class ActualizarGastoRecurrente(BaseModel):
    Concepto: Optional[str] = None
    Monto: Optional[PositiveFloat] = None
    Frecuencia: Optional[FrecuenciaEnum] = None

# =====================================
# APP
# =====================================
app = FastAPI(title="API Gastos Recurrentes")

# =====================================
# SESIÓN BASE DE DATOS
# =====================================
def obtener_db() -> Generator[Session, None, None]:
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================
# CREAR GASTO RECURRENTE
# =====================================
@app.post("/recurring-expenses", response_model=LeerGastoRecurrente)
def crear_gasto_recurrente(
    gasto: CrearGastoRecurrente,
    db: Session = Depends(obtener_db)
):
    nuevo = GastoRecurrente(
        Concepto=gasto.Concepto,
        Monto=gasto.Monto,
        FechaInicio=gasto.FechaInicio,
        Frecuencia=gasto.Frecuencia.value,
        IdCliente=gasto.IdCliente,
        Activo=True
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

# =====================================
# LISTAR
# =====================================
@app.get("/recurring-expenses", response_model=List[LeerGastoRecurrente])
def listar_gastos_recurrentes(db: Session = Depends(obtener_db)):
    return db.query(GastoRecurrente).all()

# =====================================
# OBTENER POR ID
# =====================================
@app.get("/recurring-expenses/{id}", response_model=LeerGastoRecurrente)
def obtener_gasto_por_id(id: int, db: Session = Depends(obtener_db)):
    gasto = db.query(GastoRecurrente).filter(
        GastoRecurrente.IdGastoRecurrente == id
    ).first()

    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return gasto

# =====================================
# EDITAR GASTO RECURRENTE (PFA-57)
# =====================================
@app.put("/recurring-expenses/{id}", response_model=LeerGastoRecurrente)
def actualizar_gasto_recurrente(
    id: int,
    datos: ActualizarGastoRecurrente,
    db: Session = Depends(obtener_db)
):
    gasto_actual = db.query(GastoRecurrente).filter(
        GastoRecurrente.IdGastoRecurrente == id,
        GastoRecurrente.Activo == True
    ).first()

    if not gasto_actual:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    # Desactivar registro anterior
    gasto_actual.Activo = False
    db.commit()

    # Crear nuevo registro actualizado
    nuevo_gasto = GastoRecurrente(
        Concepto=datos.Concepto or gasto_actual.Concepto,
        Monto=datos.Monto or gasto_actual.Monto,
        FechaInicio=date.today(),
        Frecuencia=datos.Frecuencia.value if datos.Frecuencia else gasto_actual.Frecuencia,
        IdCliente=gasto_actual.IdCliente,
        Activo=True
    )

    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)

    return nuevo_gasto

# =====================================
# ELIMINAR LÓGICO
# =====================================
@app.delete("/recurring-expenses/{id}")
def eliminar_gasto(id: int, db: Session = Depends(obtener_db)):
    gasto = db.query(GastoRecurrente).filter(
        GastoRecurrente.IdGastoRecurrente == id
    ).first()

    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    gasto.Activo = False
    db.commit()

    return {"message": "Gasto desactivado"}

# =====================================
# GENERAR GASTOS MENSUALES
# =====================================
@app.get("/generate-monthly-expenses")
def generar_gastos_mensuales(db: Session = Depends(obtener_db)):
    hoy = date.today()

    gastos = db.query(GastoRecurrente).filter(
        GastoRecurrente.Activo == True
    ).all()

    generados = []

    for gasto in gastos:
        if gasto.FechaInicio.day == hoy.day:
            generados.append({
                "Concepto": gasto.Concepto,
                "Monto": float(gasto.Monto),
                "Fecha": hoy
            })

    return {
        "message": "Gastos generados",
        "data": generados
    }