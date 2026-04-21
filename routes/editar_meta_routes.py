from fastapi import APIRouter
from services.editar_meta_service import MetaUpdate, editar_meta

router = APIRouter(prefix="/api/metas", tags=["Metas de Ahorro"])


@router.put("/{idMeta}")
def actualizar_meta(idMeta: int, meta: MetaUpdate):
    return editar_meta(idMeta, meta)
