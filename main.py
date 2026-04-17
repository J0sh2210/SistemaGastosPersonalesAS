from datetime import date, datetime
from typing import Generator, List, Optional
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field, PositiveFloat
from sqlalchemy import Boolean, Column, Date, DateTime, DECIMAL, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# =============================
# CONEXIÓN A BASE DE DATOS
# =============================
DATABASE_URL = (
    "mssql+pyodbc://@ENMITA\\SQLEXPRESS/SistemasGastosAS"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =============================
# ENUM
# =============================
class FrecuenciaEnum(str, Enum):
    mensual = "mensual"

# =============================
# MODELO SQL
# =============================
class Cliente(Base):
    __tablename__ = "Cliente"

    IdCliente = Column(Integer, primary_key=True, index=True)
    PrimerNombre = Column(String(100), nullable=False)
    SegundoNombre = Column(String(100), nullable=True)
    PrimerApellido = Column(String(100), nullable=False)
    SegundoApellido = Column(String(100), nullable=True)
    FechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
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

Base.metadata.create_all(bind=engine)

# =============================
# MODELOS PYDANTIC
# =============================
class RecurringExpenseCreate(BaseModel):
    Concepto: str = Field(..., min_length=1, description="Nombre del gasto")
    Monto: PositiveFloat
    FechaInicio: date
    Frecuencia: FrecuenciaEnum
    IdCliente: int

class ClienteCreate(BaseModel):
    PrimerNombre: str = Field(..., min_length=1)
    SegundoNombre: Optional[str] = None
    PrimerApellido: str = Field(..., min_length=1)
    SegundoApellido: Optional[str] = None

class ClienteRead(ClienteCreate):
    IdCliente: int
    FechaCreacion: datetime
    Estado: str

    class Config:
        orm_mode = True

class RecurringExpenseRead(RecurringExpenseCreate):
    IdGastoRecurrente: int
    is_active: bool

    class Config:
        orm_mode = True

class RecurringExpenseUpdate(BaseModel):
    Concepto: Optional[str] = Field(None, min_length=1, description="Nombre del gasto")
    Monto: Optional[PositiveFloat] = None
    FechaInicio: Optional[date] = None
    Frecuencia: Optional[FrecuenciaEnum] = None
    IdCliente: Optional[int] = None
    is_active: Optional[bool] = None

# =============================
# APP
# =============================
app = FastAPI(title="Gastos Recurrentes API")

# =============================
# DEPENDENCIA DE BASE DE DATOS
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================
# CLIENTES
@app.post("/clientes", include_in_schema=False, response_model=ClienteRead, summary="Crear cliente")
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_obj = Cliente(
        PrimerNombre=cliente.PrimerNombre,
        SegundoNombre=cliente.SegundoNombre,
        PrimerApellido=cliente.PrimerApellido,
        SegundoApellido=cliente.SegundoApellido,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@app.get("/clientes", include_in_schema=False, response_model=List[ClienteRead], summary="Listar clientes")
def list_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@app.get("/clientes/{id}", include_in_schema=False, response_model=ClienteRead, summary="Obtener cliente por ID")
def get_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.IdCliente == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# =============================
# CREAR
# =============================
@app.post("/recurring-expenses", response_model=RecurringExpenseRead, summary="Crear gasto recurrente")
def create_recurring_expense(expense: RecurringExpenseCreate, db: Session = Depends(get_db)):
    db_obj = RecurringExpense(
        Concepto=expense.Concepto,
        Monto=expense.Monto,
        FechaInicio=expense.FechaInicio,
        Frecuencia=expense.Frecuencia.value,
        IdCliente=expense.IdCliente,
        is_active=True
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# =============================
# LISTAR
# =============================
@app.get("/recurring-expenses", response_model=List[RecurringExpenseRead], summary="Listar gastos recurrentes")
def list_recurring_expenses(db: Session = Depends(get_db)):
    return db.query(RecurringExpense).all()

# =============================
# OBTENER POR ID
# =============================
@app.get("/recurring-expenses/{id}", response_model=RecurringExpenseRead, summary="Obtener gasto por ID")
def get_recurring_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return expense

# =============================
# ACTUALIZAR
@app.put("/recurring-expenses/{id}", response_model=RecurringExpenseRead, summary="Actualizar gasto recurrente")
def update_recurring_expense(
    id: int,
    expense_update: RecurringExpenseUpdate,
    db: Session = Depends(get_db)
):
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "Frecuencia":
            value = value.value
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense

# =============================
# ELIMINAR
# =============================
@app.delete("/recurring-expenses/{id}", summary="Eliminar gasto recurrente")
def delete_recurring_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    db.delete(expense)
    db.commit()

    return {"message": "Eliminado correctamente"}

# =============================
# ACTIVAR / DESACTIVAR
# =============================
@app.put("/recurring-expenses/{id}/toggle", summary="Activar o desactivar gasto")
def toggle_expense(id: int, db: Session = Depends(get_db)):
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    expense.is_active = not expense.is_active
    db.commit()

    return {"message": "Estado actualizado", "is_active": expense.is_active}

# =============================
# SIMULAR GENERACIÓN MENSUAL
# =============================
@app.get("/generate-monthly-expenses", summary="Generar gastos mensuales automáticamente")
def generate_monthly_expenses(db: Session = Depends(get_db)):
    today = date.today()
    expenses = db.query(RecurringExpense).filter(
        RecurringExpense.is_active == True
    ).all()

    generated = []
    for exp in expenses:
        if exp.FechaInicio.day == today.day:
            generated.append({
                "Concepto": exp.Concepto,
                "Monto": float(exp.Monto),
                "Fecha": today
            })

    return {
        "message": "Gastos generados",
        "data": generated
    }