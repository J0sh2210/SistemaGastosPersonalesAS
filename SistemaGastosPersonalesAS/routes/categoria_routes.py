from fastapi import APIRouter
from SistemaGastosPersonalesAS.models.categoria_model import CategoriaCreate, CategoriaUpdate
from SistemaGastosPersonalesAS.services.categoria_service import actualizar_categoria,  crear_categoria, eliminar_categoria, obtener_categorias

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/")
def crear(categoria: CategoriaCreate):
    return crear_categoria(categoria)

@router.get("/")
def listar():
    return obtener_categorias()

