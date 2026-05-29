from datetime import date
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

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
    
def actualizar_cantidad_ahorro(id_meta, data):

    # Validar que no sea negativo
    if data.monto_actual < 0:
        raise HTTPException(
            status_code=400,
            detail="La cantidad ahorrada no puede ser negativa"
        )

    try:

        query = text("""
        UPDATE MetasAhorro
        SET MontoActual = :monto_actual
        WHERE IdMeta = :id_meta
        """)

        with engine.begin() as conn:

            resultado = conn.execute(query, {
                "monto_actual": data.monto_actual,
                "id_meta": id_meta
            })

            # Verificar si existe
            if resultado.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Meta no encontrada"
                )

        return {
            "mensaje": "Cantidad de ahorro actualizada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
def eliminar_meta(id_meta):

    try:

        query = text("""
        DELETE FROM MetasAhorro
        WHERE IdMeta = :id_meta
        """)

        with engine.begin() as conn:

            resultado = conn.execute(query, {
                "id_meta": id_meta
            })

            # Verificar si existe
            if resultado.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Meta de ahorro no encontrada"
                )

        return {
            "mensaje": "Meta de ahorro eliminada correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
def obtener_metas_por_usuario(db: Session, id_usuario: int):
    # Consulta SQL para traer las metas filtrando por el ID correcto
    query = text("""
        SELECT 
            IdMeta, 
            IdUsuario, 
            NombreMeta, 
            MontoObjetivo, 
            FechaLimite, 
            MontoActual
        FROM MetasAhorro
        WHERE IdUsuario = :id_usuario
    """)
    
    # Ejecutamos la consulta pasándole el parámetro
    result = db.execute(query, {"id_usuario": id_usuario}).fetchall()
    
    # Mapeamos los resultados a una lista de diccionarios para que FastAPI los convierta a JSON
    return [row._mapping for row in result]