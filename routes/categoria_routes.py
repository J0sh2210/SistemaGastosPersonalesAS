from fastapi import APIRouter
from models.categoria_model import CategoriaCreate, CategoriaUpdate
from services.categoria_service import editar_categoria, crear_categoria, eliminar_categoria, obtener_categorias

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/")
def crear(categoria: CategoriaCreate):
    return crear_categoria(categoria)


@router.get("/")
def listar():
    return obtener_categorias()

@router.put("/{id}")
def editar(id: int, categoria: CategoriaUpdate):
    return editar_categoria(id, categoria)

@router.delete("/{id}")
def eliminar(id: int):
    return eliminar_categoria(id)
