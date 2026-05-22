from fastapi import APIRouter, status

from models.meta_model import MetaAhorroCreate
from services.meta_service import crear_meta


router = APIRouter(
    prefix="/api/metas",
    tags=["Metas Ahorro"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear(meta: MetaAhorroCreate):

    return crear_meta(meta)