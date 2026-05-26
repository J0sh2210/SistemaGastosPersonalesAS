from sqlalchemy import text
from database import engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# CREAR PRESUPUESTO
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

            result = conn.execute(query, {
                "monto": presupuesto_data.monto_presupuesto,
                "categoria": presupuesto_data.id_categoria,
                "mes": presupuesto_data.mes_aplicacion,
                "usuario": presupuesto_data.id_usuario
            })

            row = result.fetchone()
            conn.commit()

        if row:
            return {
                "id_presupuesto": row[0],
                "monto_presupuesto": float(row[1]),
                "categoria": row[2],
                "mes_aplicacion": row[3],
                "id_usuario": row[4]
            }

        return {"mensaje": "Presupuesto creado correctamente"}

    except SQLAlchemyError as e:

        error = str(e)

        if "La categoria no existe" in error:
            raise HTTPException(status_code=400, detail="La categoría no existe")

        if "El usuario no existe" in error:
            raise HTTPException(status_code=400, detail="El usuario no existe")

        if "El monto debe ser mayor a 0" in error:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")

        if "Ya existe un presupuesto" in error:
            raise HTTPException(status_code=400, detail="Ya existe un presupuesto para esta categoría y mes")

        raise HTTPException(status_code=500, detail=str(e))


# OBTENER PRESUPUESTOS
def obtener_presupuestos():

    query = text("""
        SELECT
            p.IdPresupuesto,
            p.MontoPresupuesto,
            c.NombreCategoria,
            p.MesAplicacion,
            p.IdUsuario
        FROM PresupuestoMensual p
        INNER JOIN CategoriaMovimiento c
            ON p.IdCategoria = c.IdCategoria
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            {
                "id_presupuesto": row[0],
                "monto_presupuesto": float(row[1]),
                "categoria": row[2],
                "mes_aplicacion": row[3],
                "id_usuario": row[4]
            }
            for row in result
        ]


# ACTUALIZAR PRESUPUESTO
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
        return {"mensaje": "No se enviaron datos para actualizar"}

    valores["id"] = id_presupuesto

    update_query = text(f"""
        UPDATE PresupuestoMensual
        SET {", ".join(campos)}
        WHERE IdPresupuesto = :id
    """)

    select_query = text("""
        SELECT
            p.IdPresupuesto,
            p.MontoPresupuesto,
            c.NombreCategoria,
            p.MesAplicacion,
            p.IdUsuario
        FROM PresupuestoMensual p
        INNER JOIN CategoriaMovimiento c
            ON p.IdCategoria = c.IdCategoria
        WHERE p.IdPresupuesto = :id
    """)

    with engine.connect() as conn:

        conn.execute(update_query, valores)
        conn.commit()

        result = conn.execute(select_query, {"id": id_presupuesto})
        row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")

    return {
        "id_presupuesto": row[0],
        "monto_presupuesto": float(row[1]),
        "categoria": row[2],
        "mes_aplicacion": row[3],
        "id_usuario": row[4]
    }

# ELIMINAR PRESUPUESTO
def eliminar_presupuesto(id_presupuesto):

    query = text("""
        DELETE FROM PresupuestoMensual
        WHERE IdPresupuesto = :id
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"id": id_presupuesto})
        conn.commit()

        if result.rowcount == 0:
            return {"mensaje": "Presupuesto no encontrado"}

    return {"mensaje": "Presupuesto eliminado correctamente"}


# VALIDAR PRESUPUESTO (80% ALERTA)
def validar_presupuesto(id_usuario, id_categoria):

    query = text("""
        EXEC sp_ValidarPresupuesto
            @IdUsuario = :usuario,
            @IdCategoria = :categoria
    """)

    try:
        with engine.connect() as conn:

            result = conn.execute(query, {
                "usuario": id_usuario,
                "categoria": id_categoria
            })

            row = result.fetchone()

            if not row:
                return {"mensaje": "No se encontró información"}

            return {
                "categoria": row[0],
                "estado": row[1],
                "gastado": float(row[2]),
                "limite_presupuesto": float(row[3]),
                "porcentaje_usado": float(row[4]),
                "mostrar_alerta": row[5]
            }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))