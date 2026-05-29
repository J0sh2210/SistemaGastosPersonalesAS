from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.meta_model import MetaAhorroCreate, ActualizarCantidadMeta
from services import meta_service
from services.meta_service import actualizar_cantidad_ahorro, crear_meta, eliminar_meta

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@router.delete("/{id_meta}")
def eliminar(id_meta: int):

    return eliminar_meta(id_meta)

@router.get("/{id_usuario}", status_code=status.HTTP_200_OK)
def listar_metas(id_usuario: int, db: Session = Depends(get_db)):
    try:
        # Llamamos a la capa de servicio
        metas = meta_service.obtener_metas_por_usuario(db, id_usuario)
        return metas
        
    except Exception as e:
        print(f"Error al obtener metas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener las metas de ahorro."
        )