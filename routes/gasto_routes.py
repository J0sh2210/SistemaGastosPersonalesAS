from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal # Importamos desde tu database.py
from models.schemas import GastoCreate, GastoResponse
from services import gasto_service

router = APIRouter()

# Dependencia para la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/VerGastos")
def listar_gastos(db: Session = Depends(get_db)):
    return gasto_service.obtener_gastos(db)

@router.post("/CrearGasto", response_model=GastoResponse)
def crear_gasto(gasto: GastoCreate, db: Session = Depends(get_db)):
    return gasto_service.crear_nuevo_gasto(db, gasto)

@router.put("/EditarGasto")
def editar_gasto(id_gasto: int, gasto: GastoCreate, db: Session = Depends(get_db)):
    return gasto_service.actualizar_gasto_db(db, id_gasto, gasto)

@router.delete("/BorrarGasto")
def borrar_gasto(id_gasto: int, db: Session = Depends(get_db)):
    return gasto_service.eliminar_gasto_db(db, id_gasto)