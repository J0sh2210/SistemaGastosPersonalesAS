from fastapi import APIRouter
from models.categoria_model import CategoriaCreate
from services.categoria_service import crear_categoria, obtener_categorias

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/")
def crear(categoria: CategoriaCreate):
    return crear_categoria(categoria)


@router.get("/")
def listar():
    return obtener_categorias()
