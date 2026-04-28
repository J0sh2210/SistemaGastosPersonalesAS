from database import SessionLocal
from sqlalchemy import text

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