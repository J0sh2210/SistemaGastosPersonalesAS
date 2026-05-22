from fastapi import APIRouter, status

from models.meta_model import MetaAhorroCreate, ActualizarCantidadMeta
from services.meta_service import actualizar_cantidad_ahorro, crear_meta



router = APIRouter(
    prefix="/api/metas",
    tags=["Metas Ahorro"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear(meta: MetaAhorroCreate):

    return crear_meta(meta)

@router.put("/cantidad/{id_meta}")
def actualizar_cantidad(id_meta: int, meta: ActualizarCantidadMeta):

    return actualizar_cantidad_ahorro(id_meta, meta)