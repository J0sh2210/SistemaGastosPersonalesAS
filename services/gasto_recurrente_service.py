from sqlalchemy import text
from sqlalchemy.orm import Session

from models.gasto_recurrente_model import GastoRecurrente


def desactivar_gasto_recurrente(db, id_gasto):
    gasto = db.query(GastoRecurrente)\
        .filter(GastoRecurrente.IdGastoRecurrente == id_gasto)\
        .first()

    if not gasto:
        return {"success": False, "message": "No encontrado"}

    gasto.Activo = False
    db.commit()

    return {"success": True, "message": "Desactivado correctamente"}

@staticmethod
def obtener_por_cliente(db: Session, id_cliente: int):

        query = text("""
            DELETE FROM GastoRecurrente
            WHERE IdGastoRecurrente = :IdGastoRecurrente
        """)
        

        result = db.execute(query, {"IdCliente": id_cliente}).fetchall()
        

        return [row._mapping for row in result] if result else []