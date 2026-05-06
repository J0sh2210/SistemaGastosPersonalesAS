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