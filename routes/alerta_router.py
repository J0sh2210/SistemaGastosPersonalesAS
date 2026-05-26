from fastapi import APIRouter
from models.alerta_model import AlertaCreate, AlertaUpdate
from services.alerta_service import (
    crear_alerta,
    obtener_alertas,
    actualizar_alerta,
    eliminar_alerta
)

router = APIRouter(
    prefix="/alertas",
    tags=["Alertas"]
)


# =========================
# GET
# =========================
@router.get("/")
def listar():
    return obtener_alertas()


# =========================
# POST
# =========================
@router.post("/")
def crear(data: AlertaCreate):
    return crear_alerta(data)


# =========================
# PUT
# =========================
@router.put("/{id_alerta}")
def actualizar(id_alerta: int, data: AlertaUpdate):
    return actualizar_alerta(id_alerta, data)


# =========================
# DELETE
# =========================
@router.delete("/{id_alerta}")
def eliminar(id_alerta: int):
    return eliminar_alerta(id_alerta)