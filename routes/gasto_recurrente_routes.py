from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from services.gasto_recurrente_service import desactivar_gasto_recurrente
from database import SessionLocal
from models.gasto_recurrente_model import GastoRecurrente
from models.schemas import CrearGastoRecurrente, LeerGastoRecurrente, ActualizarGastoRecurrente

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LeerGastoRecurrente)
def crear_gasto_recurrente(gasto: CrearGastoRecurrente, db: Session = Depends(get_db)):
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

@router.get("/", response_model=List[LeerGastoRecurrente])
def listar_gastos_recurrentes(db: Session = Depends(get_db)):
    return db.query(GastoRecurrente).filter(GastoRecurrente.Activo == True).all()

@router.put("/{id}", response_model=LeerGastoRecurrente)
def actualizar_gasto_recurrente(id: int, datos: ActualizarGastoRecurrente, db: Session = Depends(get_db)):
    gasto_actual = db.query(GastoRecurrente).filter(GastoRecurrente.IdGastoRecurrente == id, GastoRecurrente.Activo == True).first()
    if not gasto_actual:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    gasto_actual.Activo = False # Desactivado lógico
    db.commit()

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



@router.get("/generate-monthly")
def generar_gastos_mensuales(db: Session = Depends(get_db)):
    hoy = date.today()
    gastos = db.query(GastoRecurrente).filter(GastoRecurrente.Activo == True).all()
    generados = []
    for gasto in gastos:
        if gasto.FechaInicio.day == hoy.day:
            generados.append({"Concepto": gasto.Concepto, "Monto": float(gasto.Monto), "Fecha": hoy})
    return {"message": "Gastos procesados", "data": generados}

@router.put("/desactivar/{id}")
def desactivar(id: int, db: Session = Depends(get_db)):
    return desactivar_gasto_recurrente(db, id)