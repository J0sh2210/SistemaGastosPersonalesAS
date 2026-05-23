from fastapi import APIRouter

from models.presupuesto_model import (
    PresupuestoCreate,
    PresupuestoUpdate
)

from services.presupuesto_service import (
    crear_presupuesto_mensual,
    obtener_presupuestos,
    actualizar_presupuesto,
    eliminar_presupuesto
)

router = APIRouter(
    prefix="/presupuestos",
    tags=["Presupuestos"]
)


# CREAR
@router.post("/")
def crear_presupuesto(presupuesto_data: PresupuestoCreate):
    return crear_presupuesto_mensual(presupuesto_data)


# LISTAR
@router.get("/")
def listar_presupuestos():
    return obtener_presupuestos()


# ACTUALIZAR
@router.put("/{id_presupuesto}")
def editar_presupuesto(
    id_presupuesto: int,
    data: PresupuestoUpdate
):
    return actualizar_presupuesto(id_presupuesto, data)


# ELIMINAR
@router.delete("/{id_presupuesto}")
def eliminar(id_presupuesto: int):
    return eliminar_presupuesto(id_presupuesto)