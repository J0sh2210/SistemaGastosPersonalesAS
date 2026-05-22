from datetime import date
from fastapi import HTTPException
from sqlalchemy import text

from database import engine


def crear_meta(data):

    # Validar nombre
    if not data.nombre_meta.strip():
        raise HTTPException(
            status_code=400,
            detail="El nombre de la meta no puede estar vacío"
        )

    # Validar monto objetivo
    if data.monto_objetivo <= 0:
        raise HTTPException(
            status_code=400,
            detail="El monto objetivo debe ser mayor a cero"
        )

    # Validar fecha
    if data.fecha_limite < date.today():
        raise HTTPException(
            status_code=400,
            detail="La fecha límite no puede ser anterior a hoy"
        )

    # Validar monto actual
    if data.monto_actual < 0:
        raise HTTPException(
            status_code=400,
            detail="El monto actual no puede ser negativo"
        )

    try:

        query = text("""
        EXEC sp_CrearMetaAhorro
            @IdUsuario = :id_usuario,
            @NombreMeta = :nombre_meta,
            @MontoObjetivo = :monto_objetivo,
            @FechaLimite = :fecha_limite,
            @MontoActual = :monto_actual
        """)

        with engine.begin() as conn:

            resultado = conn.execute(query, {
                "id_usuario": data.id_usuario,
                "nombre_meta": data.nombre_meta,
                "monto_objetivo": data.monto_objetivo,
                "fecha_limite": data.fecha_limite,
                "monto_actual": data.monto_actual
            })

            id_meta = resultado.fetchone()[0]

        return {
            "mensaje": "Meta creada correctamente",
            "id_meta": int(id_meta)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )