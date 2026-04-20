from database import engine
from sqlalchemy import text
from fastapi import HTTPException


# CREA LAS CATEGORIAS
def crear_categoria(data):
    query = text("""
        INSERT INTO CategoriaMovimiento (NombreCategoria, IdTipoMovimiento, IdTipoCategoria)
        VALUES (:nombre, :tipo_mov, :tipo_cat)
    """)

    with engine.begin() as conn:
        conn.execute(query, {
            "nombre": data.nombre_categoria,
            "tipo_mov": data.id_tipo_movimiento,
            "tipo_cat": data.id_tipo_categoria
        })

    return {"mensaje": "Categoría creada correctamente"}


# ENLISTA LAS CATEGORIAS
def obtener_categorias():
    query = text("""
        SELECT c.IdCategoria, c.NombreCategoria, tm.Nombre, tcm.NombreTipo
        FROM CategoriaMovimiento c
        INNER JOIN TipoMovimiento tm ON c.IdTipoMovimiento = tm.IdTipo
        INNER JOIN TipoCategoriaMovimiento tcm ON c.IdTipoCategoria = tcm.IdTipoCategoria
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        return [
            {
                "id": row[0],
                "nombre": row[1],
                "tipo_movimiento": row[2],
                "tipo_categoria": row[3]
            }
            for row in result
        ]

# ACTUALIZA LAS CATEGORIAS
def editar_categoria(id, data):

    campos = []
    valores = {"id": id}

    # NOMBRE
    if data.nombre_categoria is not None:
        campos.append("NombreCategoria = :nombre")
        valores["nombre"] = data.nombre_categoria

    # TIPO MOVIMIENTO
    if data.id_tipo_movimiento is not None:

        if data.id_tipo_movimiento <= 0:
            raise HTTPException(
                status_code=400,
                detail="IdTipoMovimiento inválido"
            )

        if not existe_tipo_movimiento(data.id_tipo_movimiento):
            raise HTTPException(
                status_code=400,
                detail="TipoMovimiento no existe"
            )

        campos.append("IdTipoMovimiento = :tipo_mov")
        valores["tipo_mov"] = data.id_tipo_movimiento

    # TIPO CATEGORIA
    if data.id_tipo_categoria is not None:

        if data.id_tipo_categoria <= 0:
            raise HTTPException(
                status_code=400,
                detail="IdTipoCategoria inválido"
            )

        if not existe_tipo_categoria(data.id_tipo_categoria):
            raise HTTPException(
                status_code=400,
                detail="TipoCategoria no existe"
            )

        campos.append("IdTipoCategoria = :tipo_cat")
        valores["tipo_cat"] = data.id_tipo_categoria

    # SI NO VIENE NADA
    if not campos:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    query = text(f"""
    UPDATE CategoriaMovimiento
    SET {', '.join(campos)}
    WHERE IdCategoria = :id
    """)

    with engine.begin() as conn:
        resultado = conn.execute(query, valores)

        if resultado.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

    return {"mensaje": "Categoría actualizada correctamente"}



# VALIDACIONES FK
def existe_tipo_movimiento(id_tipo):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM TipoMovimiento WHERE IdTipo = :id"),
            {"id": id_tipo}
        ).fetchone()

        return result is not None


def existe_tipo_categoria(id_tipo):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM TipoCategoriaMovimiento WHERE IdTipoCategoria = :id"),
            {"id": id_tipo}
        ).fetchone()

        return result is not None
