from fastapi import APIRouter
from models.meta_model import MetaCreate
from services.meta_service import crear_meta, eliminar_meta

router = APIRouter(prefix="/api/metas", tags=["Metas de Ahorro"])


@router.post("/")
def crear(meta: MetaCreate):
    return crear_meta(meta)


@router.delete("/{idMeta}")
def eliminar(idMeta: int, idUsuario: int, confirmar: bool = False):
    return eliminar_meta(idMeta, idUsuario, confirmar)
