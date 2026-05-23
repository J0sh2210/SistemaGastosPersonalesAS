from sqlalchemy import text
from database import engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


# CREAR
def crear_presupuesto_mensual(presupuesto_data):

    query = text("""
        EXEC sp_CrearPresupuesto
            @MontoPresupuesto = :monto,
            @IdCategoria = :categoria,
            @MesAplicacion = :mes,
            @IdUsuario = :usuario
    """)

    try:

        with engine.connect() as conn:

            conn.execute(query, {
                "monto": presupuesto_data.monto_presupuesto,
                "categoria": presupuesto_data.id_categoria,
                "mes": presupuesto_data.mes_aplicacion,
                "usuario": presupuesto_data.id_usuario
            })

            conn.commit()

        return {
            "mensaje": "Presupuesto creado correctamente"
        }

    except SQLAlchemyError as e:

        error = str(e)

        if "La categoria no existe" in error:
            raise HTTPException(
                status_code=400,
                detail="La categoría seleccionada no existe"
            )

        if "El usuario no existe" in error:
            raise HTTPException(
                status_code=400,
                detail="El usuario no existe"
            )

        if "El monto debe ser mayor a 0" in error:
            raise HTTPException(
                status_code=400,
                detail="El monto debe ser mayor a 0"
            )

        raise HTTPException(
        status_code=500,
        detail=str(e)
    )
# ACTUALIZAR
def actualizar_presupuesto(id_presupuesto, data):

    campos = []
    valores = {}

    if data.monto_presupuesto is not None:
        campos.append("MontoPresupuesto = :monto")
        valores["monto"] = data.monto_presupuesto

    if data.id_categoria is not None:
        campos.append("IdCategoria = :categoria")
        valores["categoria"] = data.id_categoria

    if data.mes_aplicacion is not None:
        campos.append("MesAplicacion = :mes")
        valores["mes"] = data.mes_aplicacion

    if data.id_usuario is not None:
        campos.append("IdUsuario = :usuario")
        valores["usuario"] = data.id_usuario

    if not campos:
        return {
            "mensaje": "No se enviaron datos para actualizar"
        }

    valores["id"] = id_presupuesto

    query = text(f"""
        UPDATE PresupuestoMensual
        SET {", ".join(campos)}
        WHERE IdPresupuesto = :id
    """)

    with engine.connect() as conn:

        result = conn.execute(query, valores)

        conn.commit()

        if result.rowcount == 0:
            return {
                "mensaje": "Presupuesto no encontrado"
            }

    return {
        "mensaje": "Presupuesto actualizado correctamente"
    }


# ELIMINAR
def eliminar_presupuesto(id_presupuesto):

    query = text("""
        DELETE FROM PresupuestoMensual
        WHERE IdPresupuesto = :id
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {
            "id": id_presupuesto
        })

        conn.commit()

        if result.rowcount == 0:
            return {
                "mensaje": "Presupuesto no encontrado"
            }

    return {
        "mensaje": "Presupuesto eliminado correctamente"
    }

# OBTENER PRESUPUESTOS
def obtener_presupuestos():

    query = text("""
        SELECT
            IdPresupuesto,
            MontoPresupuesto,
            IdCategoria,
            MesAplicacion,
            IdUsuario
        FROM PresupuestoMensual
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        presupuestos = []

        for row in result:
            presupuestos.append({
                "id_presupuesto": row[0],
                "monto_presupuesto": float(row[1]),
                "id_categoria": row[2],
                "mes_aplicacion": row[3],
                "id_usuario": row[4]
            })

    return presupuestos