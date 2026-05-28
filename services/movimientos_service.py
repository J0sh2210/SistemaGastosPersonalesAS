from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text

class MovimientoService:
    @staticmethod
    def obtener_movimientos_mes_actual(db: Session, id_cliente: int):
        # Ejecutamos el SP pasando el IdCliente
        query = text("EXEC sp_ObtenerMovimientosMesActual @IdCliente = :IdCliente")
        result = db.execute(query, {"IdCliente": id_cliente}).fetchall()
        
        # Mapeamos los resultados para que Pydantic los pueda leer fácilmente
        return [row._mapping for row in result]

def editar_categoria_movimiento(idMovimiento: int, idCategoria: int):
    db = SessionLocal()
    try:
        # Validar movimiento
        movimiento = db.execute(
            text("SELECT 1 FROM Movimiento WHERE IdMovimiento = :id"),
            {"id": idMovimiento}
        ).fetchone()

        if not movimiento:
            return "MOVIMIENTO_NO_EXISTE"

        # Validar categoria
        categoria = db.execute(
            text("SELECT 1 FROM CategoriaMovimiento WHERE IdCategoria = :id"),
            {"id": idCategoria}
        ).fetchone()

        if not categoria:
            return "CATEGORIA_NO_EXISTE"


        db.execute(
            text("""
                UPDATE Movimiento
                SET IdCategoria = :idCategoria
                WHERE IdMovimiento = :idMovimiento
            """),
            {
                "idMovimiento": idMovimiento,
                "idCategoria": idCategoria
            }
        )

        db.commit()
        return "OK"

    finally:
        db.close()

def calcular_diferencia(tipo: str):
    db = SessionLocal()

    if tipo == "mes":
        query = text("""
            SELECT 
                YEAR(m.FechaMovimiento) AS Anio,
                MONTH(m.FechaMovimiento) AS Mes,
                SUM(
                    CASE 
                        WHEN tm.Nombre = 'Ingreso' THEN m.Monto
                        WHEN tm.Nombre = 'Egreso' THEN -m.Monto
                        ELSE 0
                    END
                ) AS Total
            FROM Movimiento m
            INNER JOIN TipoMovimiento tm 
                ON m.IdTipo = tm.IdTipo
            GROUP BY 
                YEAR(m.FechaMovimiento),
                MONTH(m.FechaMovimiento)
            ORDER BY 
                Anio, Mes
        """)
    else:  # año
        query = text("""
            SELECT 
                YEAR(m.FechaMovimiento) AS Anio,
                SUM(
                    CASE 
                        WHEN tm.Nombre = 'Ingreso' THEN m.Monto
                        WHEN tm.Nombre = 'Egreso' THEN -m.Monto
                        ELSE 0
                    END
                ) AS Total
            FROM Movimiento m
            INNER JOIN TipoMovimiento tm 
                ON m.IdTipo = tm.IdTipo
            GROUP BY 
                YEAR(m.FechaMovimiento)
            ORDER BY 
                Anio
        """)

    resultado = db.execute(query).fetchall()
    db.close()

    data = []
    for row in resultado:
        if tipo == "mes":
            data.append({
                "anio": row.Anio,
                "mes": row.Mes,
                "total": float(row.Total)
            })
        else:
            data.append({
                "anio": row.Anio,
                "total": float(row.Total)
            })

    return data

def filtrar_movimientos(db: Session, id_cliente, id_tipo=None, fecha_inicio=None, fecha_fin=None):
    # 1. Empezamos con la consulta base, uniendo con TipoMovimiento por si necesitas el nombre
    base_query = """
        SELECT 
            m.IdMovimiento,
            m.Concepto,
            m.Monto,
            m.FechaMovimiento,
            m.IdCliente,
            m.IdTipo,
            m.IdCategoria,
            tm.Nombre AS NombreTipoMovimiento
        FROM Movimiento m
        LEFT JOIN TipoMovimiento tm ON m.IdTipo = tm.IdTipo
        WHERE m.IdCliente = :id_cliente
        
    """
    
    # 2. Preparamos el diccionario de parámetros obligatorios
    params = {"id_cliente": id_cliente}

    # 3. Agregamos condiciones extra solo si se enviaron parámetros
    if id_tipo is not None:
        base_query += " AND m.IdTipo = :id_tipo"
        params["id_tipo"] = id_tipo

    if fecha_inicio is not None:
        base_query += " AND CAST(m.FechaMovimiento AS DATE) >= :fecha_inicio"
        params["fecha_inicio"] = fecha_inicio

    if fecha_fin is not None:
        base_query += " AND CAST(m.FechaMovimiento AS DATE) <= :fecha_fin"
        params["fecha_fin"] = fecha_fin

    # 4. Ordenamos para que salgan los más recientes primero
    base_query += " ORDER BY m.FechaMovimiento DESC"

    # 5. Ejecutamos la consulta dinámica
    query = text(base_query)
    result = db.execute(query, params).fetchall()

    return [dict(row._mapping) for row in result]