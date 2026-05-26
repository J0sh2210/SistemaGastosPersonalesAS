from sqlalchemy import text
from database import engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


# =========================
# OBTENER ALERTAS
# =========================
def obtener_alertas():

    query = text("""
        SELECT
            IdAlerta,
            IdUsuario,
            IdCategoria,
            TipoAlerta,
            Mensaje,
            Gastado,
            LimitePresupuesto,
            Porcentaje,
            Mes,
            Anio,
            FechaCreacion
        FROM Alerta
        ORDER BY FechaCreacion DESC
    """)

    try:
        with engine.connect() as conn:
            result = conn.execute(query)

            return [
                {
                    "id_alerta": row[0],
                    "id_usuario": row[1],
                    "id_categoria": row[2],
                    "tipo_alerta": row[3],
                    "mensaje": row[4],
                    "gastado": float(row[5]),
                    "limite_presupuesto": float(row[6]),
                    "porcentaje": float(row[7]),
                    "mes": row[8],
                    "anio": row[9],
                    "fecha_creacion": row[10]
                }
                for row in result
            ]

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# CREAR ALERTA (POST)
# =========================
def crear_alerta(data):

    query = text("""
        INSERT INTO Alerta
        (
            IdUsuario,
            IdCategoria,
            TipoAlerta,
            Mensaje,
            Gastado,
            LimitePresupuesto,
            Porcentaje,
            Mes,
            Anio
        )
        VALUES
        (
            :usuario,
            :categoria,
            :tipo,
            :mensaje,
            :gastado,
            :limite,
            :porcentaje,
            :mes,
            :anio
        )
    """)

    try:
        with engine.connect() as conn:
            conn.execute(query, {
                "usuario": data.id_usuario,
                "categoria": data.id_categoria,
                "tipo": data.tipo_alerta,
                "mensaje": data.mensaje,
                "gastado": data.gastado,
                "limite": data.limite_presupuesto,
                "porcentaje": data.porcentaje,
                "mes": data.mes,
                "anio": data.anio
            })
            conn.commit()

        return {"mensaje": "Alerta creada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ACTUALIZAR ALERTA (PUT)
# =========================
def actualizar_alerta(id_alerta, data):

    campos = []
    valores = {"id": id_alerta}

    if data.tipo_alerta is not None:
        campos.append("TipoAlerta = :tipo")
        valores["tipo"] = data.tipo_alerta

    if data.mensaje is not None:
        campos.append("Mensaje = :mensaje")
        valores["mensaje"] = data.mensaje

    if data.gastado is not None:
        campos.append("Gastado = :gastado")
        valores["gastado"] = data.gastado

    if data.limite_presupuesto is not None:
        campos.append("LimitePresupuesto = :limite")
        valores["limite"] = data.limite_presupuesto

    if data.porcentaje is not None:
        campos.append("Porcentaje = :porcentaje")
        valores["porcentaje"] = data.porcentaje

    if data.mes is not None:
        campos.append("Mes = :mes")
        valores["mes"] = data.mes

    if data.anio is not None:
        campos.append("Anio = :anio")
        valores["anio"] = data.anio

    if not campos:
        return {"mensaje": "No hay datos para actualizar"}

    query = text(f"""
        UPDATE Alerta
        SET {", ".join(campos)}
        WHERE IdAlerta = :id
    """)

    try:
        with engine.connect() as conn:
            conn.execute(query, valores)
            conn.commit()

        return {"mensaje": "Alerta actualizada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ELIMINAR ALERTA (DELETE)
# =========================
def eliminar_alerta(id_alerta):

    query = text("""
        DELETE FROM Alerta
        WHERE IdAlerta = :id
    """)

    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"id": id_alerta})
            conn.commit()

            if result.rowcount == 0:
                return {"mensaje": "Alerta no encontrada"}

        return {"mensaje": "Alerta eliminada correctamente"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))