from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract, text
from database import SessionLocal


from models.movimiento_model import Movimiento, EditarCategoriaRequest, EditarCategoriaResponse, DiferenciaResponse
from models.usuario_model import Usuario, Cliente
from services.auth_service import get_current_user
from services.movimientos_service import editar_categoria_movimiento, calcular_diferencia, filtrar_movimientos
from models.schemas import MovimientoMesResponse
from services.movimientos_service import MovimientoService
from datetime import date

router = APIRouter(tags=["Movimientos"])

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

@router.put("/Categoria", response_model=EditarCategoriaResponse)

def editar_categoria_Movimiento(idMovimiento: int, request: EditarCategoriaRequest):
    
    resultado = editar_categoria_movimiento(idMovimiento, request.idCategoria)

    if resultado == "MOVIMIENTO_NO_EXISTE":
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    if resultado == "CATEGORIA_NO_EXISTE":
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return {"message": "Categoría actualizada correctamente"}

@router.get("/diferencia")
def obtener_diferencia(tipo: str = Query(..., enum=["mes", "anio"])):
    return calcular_diferencia(tipo)

@router.get("/mes-actual/{id_cliente}", response_model=list[MovimientoMesResponse])
def obtener_movimientos_mes(id_cliente: int, db: Session = Depends(get_db)):
    movimientos = MovimientoService.obtener_movimientos_mes_actual(db, id_cliente)
    return movimientos

@router.get("/informe")
def generar_informe(
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

    total_ingresos = 0
    total_egresos = 0

    for mov in movimientos:
        if mov.IdTipo == 1:
            total_ingresos += float(mov.Monto)
        elif mov.IdTipo == 2:
            total_egresos += float(mov.Monto)

    return {
        "usuario": usuario.NombreUsuario,
        "mes": mes,
        "anio": anio,
        "totalIngresos": total_ingresos,
        "totalEgresos": total_egresos,
        "balance": total_ingresos - total_egresos
    }

""" Filtra movimientos por tipo y rango de fechas.
Permite consultas dinámicas del historial del usuario autenticado. """

@router.get("/filtrar", summary="Filtrar historial de movimientos")
def filtrar_historial_movimientos(
    id_tipo: int = None,
    fecha_inicio: date = None,
    fecha_fin: date = None,
    db: Session = Depends(get_db),
    usuario_actual: str = Depends(get_current_user)
):
    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha_inicio no puede ser mayor que fecha_fin"
        )

    usuario = db.query(Usuario).filter(
        Usuario.NombreUsuario == usuario_actual
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    resultado = filtrar_movimientos(
        db,
        usuario.IdCliente,
        id_tipo,
        fecha_inicio,
        fecha_fin
    )

    if not resultado:
        return {
            "total": 0,
            "movimientos": [],
            "message": "No se encontraron movimientos"
        }

    return {
        "total": len(resultado),
        "movimientos": resultado
    }