from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from database import SessionLocal

from models.movimiento_model import Movimiento
from models.usuario_model import Usuario, Cliente
from services.auth_service import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/mensual")
def obtener_movimientos_mensuales(
    mes: int,
    anio: int,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(
        Usuario.NombreUsuario == usuario_actual
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cliente = db.query(Cliente).filter(
        Cliente.IdCliente == usuario.IdCliente
    ).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    movimientos = db.query(Movimiento).filter(
        Movimiento.IdCliente == cliente.IdCliente,
        extract("month", Movimiento.FechaMovimiento) == mes,
        extract("year", Movimiento.FechaMovimiento) == anio
    ).all()

    ingresos = []
    egresos = []
    total_ingresos = 0
    total_egresos = 0

    for mov in movimientos:
        item = {
            "idMovimiento": mov.IdMovimiento,
            "concepto": mov.Concepto,
            "monto": float(mov.Monto),
            "fechaMovimiento": mov.FechaMovimiento,
            "idTipo": mov.IdTipo
        }

        if mov.IdTipo == 1:
            ingresos.append(item)
            total_ingresos += float(mov.Monto)
        elif mov.IdTipo == 2:
            egresos.append(item)
            total_egresos += float(mov.Monto)

    return {
        "mes": mes,
        "anio": anio,
        "cliente": cliente.IdCliente,
        "ingresos": ingresos,
        "egresos": egresos,
        "totalIngresos": total_ingresos,
        "totalEgresos": total_egresos,
        "balance": total_ingresos - total_egresos
    }