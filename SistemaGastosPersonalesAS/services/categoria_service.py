from SistemaGastosPersonalesAS.database import engine
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
