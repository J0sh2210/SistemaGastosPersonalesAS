from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime

from database import SessionLocal
from models.gasto_recurrente_model import GastoRecurrente
from models.movimiento_model import Movimiento
from models.schemas import (
    CrearGastoRecurrente,
    LeerGastoRecurrente,
    ActualizarGastoRecurrente
)
from services.gasto_recurrente_service import desactivar_gasto_recurrente

router = APIRouter()


# ------------------------
# DB Dependency
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# CREATE GASTO RECURRENTE
# ------------------------
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


# ------------------------
# LISTAR GASTOS RECURRENTES
# ------------------------
@router.get("/", response_model=List[LeerGastoRecurrente])
def listar_gastos_recurrentes(db: Session = Depends(get_db)):
    return db.query(GastoRecurrente).filter(
        GastoRecurrente.Activo == True
    ).all()


# ------------------------
# ACTUALIZAR (REEMPLAZO LÓGICO)
# ------------------------
@router.put("/{id}", response_model=LeerGastoRecurrente)
def actualizar_gasto_recurrente(id: int, datos: ActualizarGastoRecurrente, db: Session = Depends(get_db)):

    gasto_actual = db.query(GastoRecurrente).filter(
        GastoRecurrente.IdGastoRecurrente == id,
        GastoRecurrente.Activo == True
    ).first()

    if not gasto_actual:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    gasto_actual.Activo = False
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


# ------------------------
# GENERAR GASTOS MENSUALES (CORRECTO)
# ------------------------
@router.get("/generate-monthly")
def generar_gastos_mensuales(db: Session = Depends(get_db)):

    hoy = date.today()
    inicio_mes = datetime(hoy.year, hoy.month, 1)

    gastos = db.query(GastoRecurrente).filter(
        GastoRecurrente.Activo == True
    ).all()

    generados = []

    for gasto in gastos:

        # Evitar duplicados en el mismo mes
        existe = db.query(Movimiento).filter(
            Movimiento.Concepto == gasto.Concepto,
            Movimiento.IdCliente == gasto.IdCliente,
            Movimiento.FechaMovimiento >= inicio_mes
        ).first()

        if not existe:

            nuevo = Movimiento(
                Concepto=gasto.Concepto,
                Monto=gasto.Monto,
                FechaMovimiento=datetime.now(),
                IdCliente=gasto.IdCliente,
                IdTipo=2  # egreso
            )

            db.add(nuevo)

            generados.append({
                "Concepto": gasto.Concepto,
                "Monto": float(gasto.Monto),
                "Fecha": hoy
            })

    db.commit()

    return {
        "message": "Gastos mensuales generados correctamente",
        "data": generados
    }


# ------------------------
# DESACTIVAR GASTO
# ------------------------
@router.put("/desactivar/{id}")
def desactivar(id: int, db: Session = Depends(get_db)):
    return desactivar_gasto_recurrente(db, id)