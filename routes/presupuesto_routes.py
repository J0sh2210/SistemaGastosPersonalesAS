from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.schemas import PresupuestoCreate, PresupuestoUpdate, PresupuestoResponse
from services.presupuesto_service import (
    crear_presupuesto_mensual, 
    obtener_presupuesto_mensual, 
    actualizar_presupuesto_mensual, 
    eliminar_presupuesto_mensual, 
    listar_presupuestos_cliente
)

router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PresupuestoResponse, status_code=201)
def crear_presupuesto(presupuesto_data: PresupuestoCreate, db: Session = Depends(get_db)):
    return crear_presupuesto_mensual(db, presupuesto_data)

@router.get("/{id_cliente}/{anio}/{mes}", response_model=PresupuestoResponse)
def get_presupuesto(id_cliente: int, anio: int, mes: int, db: Session = Depends(get_db)):
    return obtener_presupuesto_mensual(db, id_cliente, anio, mes)

@router.get("/cliente/{id_cliente}", response_model=List[PresupuestoResponse])
def listar_por_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return listar_presupuestos_cliente(db, id_cliente)

@router.put("/{id_presupuesto}", response_model=PresupuestoResponse)
def update_presupuesto(id_presupuesto: int, update_data: PresupuestoUpdate, db: Session = Depends(get_db)):
    return actualizar_presupuesto_mensual(db, id_presupuesto, update_data)

@router.delete("/{id_presupuesto}")
def delete_presupuesto(id_presupuesto: int, db: Session = Depends(get_db)):
    return eliminar_presupuesto_mensual(db, id_presupuesto)
