from typing import Optional
from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    nombre_categoria: str
    id_tipo_movimiento: int
    id_tipo_categoria: int

# PARA EDITAR SOLO LOS CAMPOS QUE SEAN ENVIADOS
class CategoriaUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    id_tipo_movimiento: Optional[int] = None
    id_tipo_categoria: Optional[int] = None