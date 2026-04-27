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