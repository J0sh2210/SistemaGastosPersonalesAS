from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.schemas import IngresoCreate, IngresoUpdate, IngresoResponse
from services.ingreso_service import IngresoService
from typing import List

router = APIRouter(prefix="/ingresos", tags=["Ingresos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=IngresoResponse, status_code=201)
def registrar_ingreso(ingreso: IngresoCreate, db: Session = Depends(get_db)):
    return IngresoService.registrar(db, ingreso)

@router.put("/{id_ingreso}", response_model=IngresoResponse)
def editar_ingreso(id_ingreso: int, ingreso: IngresoUpdate, db: Session = Depends(get_db)):
    return IngresoService.editar(db, id_ingreso, ingreso)

@router.get("/{id_cliente}", response_model=List[IngresoResponse])
def listar_movimientos_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return IngresoService.obtener_por_cliente(db, id_cliente)
