from database import engine
from sqlalchemy import text
from fastapi import HTTPException
from datetime import date


def crear_meta(data):
    if not data.nombreMeta.strip():
        raise HTTPException(status_code=400, detail="Nombre obligatorio")
    if data.montoObjetivo <= 0:
        raise HTTPException(status_code=400, detail="Monto objetivo invalido")
    if data.fechaLimite < date.today():
        raise HTTPException(status_code=400, detail="Fecha invalida")
    if data.montoActual < 0:
        raise HTTPException(status_code=400, detail="Monto actual invalido")

    with engine.begin() as conn:
        conn.execute(text("""
            EXEC sp_CrearMetaAhorro
                @IdUsuario     = :idUsuario,
                @NombreMeta    = :nombreMeta,
                @MontoObjetivo = :montoObjetivo,
                @FechaLimite   = :fechaLimite,
                @MontoActual   = :montoActual
        """), {
            "idUsuario": data.idUsuario,
            "nombreMeta": data.nombreMeta,
            "montoObjetivo": data.montoObjetivo,
            "fechaLimite": data.fechaLimite,
            "montoActual": data.montoActual
        })

    return {"mensaje": "Meta creada correctamente"}


def eliminar_meta(idMeta: int, idUsuario: int, confirmar: bool):
    if not confirmar:
        raise HTTPException(status_code=400, detail="Debes confirmar la eliminacion")

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT IdUsuario FROM MetasAhorro WHERE IdMeta = :idMeta"),
            {"idMeta": idMeta}
        ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    if result[0] != idUsuario:
        raise HTTPException(status_code=403, detail="No autorizado")

    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM MetasAhorro WHERE IdMeta = :idMeta"),
            {"idMeta": idMeta}
        )

    return {"mensaje": "Meta eliminada correctamente"}
