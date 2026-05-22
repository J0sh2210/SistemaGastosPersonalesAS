from pydantic import BaseModel
from datetime import date


class MetaAhorroCreate(BaseModel):
    id_usuario: int
    nombre_meta: str
    monto_objetivo: float
    fecha_limite: date
    monto_actual: float

class ActualizarCantidadMeta(BaseModel):
    monto_actual: float