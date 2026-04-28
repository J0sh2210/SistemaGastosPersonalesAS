from fastapi import APIRouter
from models.gasto_model import GastoCreate, GastoUpdate
from services.gasto_service import crear_gasto, editar_gasto, obtener_gastos, obtener_gasto, eliminar_gasto

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/")
def registrar(gasto: GastoCreate):
    return crear_gasto(gasto)


@router.put("/{id}")
def editar(id: int, gasto: GastoUpdate):
    return editar_gasto(id, gasto)


@router.get("/")
def listar():
    return obtener_gastos()


@router.get("/{id}")
def consultar(id: int):
    return obtener_gasto(id)


@router.delete("/{id}")
def eliminar(id: int):
    return eliminar_gasto(id)

