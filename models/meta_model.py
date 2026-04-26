from pydantic import BaseModel
from datetime import date


class MetaCreate(BaseModel):
    idUsuario: int
    nombreMeta: str
    montoObjetivo: float
    fechaLimite: date
    montoActual: float
