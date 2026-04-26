from database import engine
from sqlalchemy import text
from fastapi import HTTPException
from datetime import date
from typing import Optional
from pydantic import BaseModel


class MetaUpdate(BaseModel):
    idUsuario: int
    nombreMeta: Optional[str] = None
    montoObjetivo: Optional[float] = None
    fechaLimite: Optional[date] = None
    montoActual: Optional[float] = None


def editar_meta(idMeta: int, data: MetaUpdate):
    # Validar que existe y es del usuario
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT IdUsuario FROM MetasAhorro WHERE IdMeta = :idMeta"),
            {"idMeta": idMeta}
        ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    if result[0] != data.idUsuario:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Validaciones
    if data.nombreMeta is not None and not data.nombreMeta.strip():
        raise HTTPException(status_code=400, detail="Nombre no puede estar vacio")
    if data.montoObjetivo is not None and data.montoObjetivo <= 0:
        raise HTTPException(status_code=400, detail="Monto objetivo invalido")
    if data.fechaLimite is not None and data.fechaLimite < date.today():
        raise HTTPException(status_code=400, detail="Fecha invalida")
    if data.montoActual is not None and data.montoActual < 0:
        raise HTTPException(status_code=400, detail="Monto actual invalido")

    # Construir campos a actualizar
    campos = []
    valores = {"idMeta": idMeta}

    if data.nombreMeta is not None:
        campos.append("NombreMeta = :nombreMeta")
        valores["nombreMeta"] = data.nombreMeta
    if data.montoObjetivo is not None:
        campos.append("MontoObjetivo = :montoObjetivo")
        valores["montoObjetivo"] = data.montoObjetivo
    if data.fechaLimite is not None:
        campos.append("FechaLimite = :fechaLimite")
        valores["fechaLimite"] = data.fechaLimite
    if data.montoActual is not None:
        campos.append("MontoActual = :montoActual")
        valores["montoActual"] = data.montoActual

    if not campos:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    with engine.begin() as conn:
        conn.execute(text(f"""
            UPDATE MetasAhorro
            SET {', '.join(campos)}
            WHERE IdMeta = :idMeta
        """), valores)

    return {"mensaje": "Meta actualizada correctamente"}
