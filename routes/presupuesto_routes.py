from fastapi import APIRouter

from models.presupuesto_model import (
    PresupuestoCreate,
    PresupuestoUpdate,
    ValidarPresupuestoResponse,
    PresupuestoResponse
)

from services.presupuesto_service import (
    crear_presupuesto_mensual,
    obtener_presupuestos,
    actualizar_presupuesto,
    eliminar_presupuesto,
    validar_presupuesto
)

router = APIRouter(
    prefix="/presupuestos",
    tags=["Presupuestos"]
)

# CREAR
@router.post("/", response_model=PresupuestoResponse)
def crear_presupuesto(presupuesto_data: PresupuestoCreate):
    return crear_presupuesto_mensual(presupuesto_data)

# LISTAR
@router.get("/", response_model=list[PresupuestoResponse])
def listar_presupuestos():
    return obtener_presupuestos()

# ACTUALIZAR
@router.put("/{id_presupuesto}", response_model=PresupuestoResponse)
def editar_presupuesto(
    id_presupuesto: int,
    data: PresupuestoUpdate
):
    return actualizar_presupuesto(id_presupuesto, data)

# ELIMINAR
@router.delete("/{id_presupuesto}")
def eliminar(id_presupuesto: int):
    return eliminar_presupuesto(id_presupuesto)

# VALIDAR PRESUPUESTO (ALERTA 80%)
@router.get(
    "/validar/{id_usuario}/{id_categoria}",
    response_model=ValidarPresupuestoResponse
)
def validar(
    id_usuario: int,
    id_categoria: int
):
    return validar_presupuesto(id_usuario, id_categoria)