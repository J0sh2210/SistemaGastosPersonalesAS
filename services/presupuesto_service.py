from sqlalchemy import text
from database import engine
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from database import SessionLocal

# ==========================================
# CREAR PRESUPUESTO
# ==========================================
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
            with conn.begin():
                result = conn.execute(query, {
                    "monto": presupuesto_data.monto_presupuesto,
                    "categoria": presupuesto_data.id_categoria,
                    "mes": presupuesto_data.mes_aplicacion,
                    "usuario": presupuesto_data.id_usuario
                })
                row = result.fetchone()

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


# ==========================================
# OBTENER PRESUPUESTOS
# ==========================================
def obtener_presupuestos():
    db = SessionLocal() 
    
    try:
        # Usamos INNER JOIN con CategoriaMovimiento para traer el NombreCategoria real sin errores
        query = """
            SELECT 
                p.IdPresupuesto, 
                p.MontoPresupuesto, 
                c.NombreCategoria, 
                p.IdCategoria, 
                p.MesAplicacion, 
                p.IdUsuario 
            FROM PresupuestoMensual p
            INNER JOIN CategoriaMovimiento c ON p.IdCategoria = c.IdCategoria
        """
        
        result = db.execute(text(query)) 
        
        presupuestos = []
        for row in result:
            presupuestos.append({
                "id_presupuesto": row[0],
                "monto_presupuesto": row[1],
                "categoria": row[2],       
                "id_categoria": row[3],    
                "mes_aplicacion": row[4],
                "id_usuario": row[5]
            })
        return presupuestos
        
    finally:
        db.close()


# ==========================================
# ACTUALIZAR PRESUPUESTO
# ==========================================
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

    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(update_query, valores)
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
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# ELIMINAR PRESUPUESTO
# ==========================================
def eliminar_presupuesto(id_presupuesto):

    query = text("""
        DELETE FROM PresupuestoMensual
        WHERE IdPresupuesto = :id
    """)

    try:
        with engine.connect() as conn:
            with conn.begin():
                result = conn.execute(query, {"id": id_presupuesto})

                if result.rowcount == 0:
                    return {"mensaje": "Presupuesto no encontrado"}

        return {"mensaje": "Presupuesto eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))