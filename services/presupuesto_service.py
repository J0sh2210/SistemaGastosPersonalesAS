from fastapi import HTTPException
from typing import List
from datetime import datetime
from models.presupuesto_model import PresupuestoResponse, PresupuestoCreate, PresupuestoUpdate

# Global mock storage (simula DB - persistente memoria)
_presupuestos_mock = {}

def crear_presupuesto_mensual(db, presupuesto_data: PresupuestoCreate) -> PresupuestoResponse:
    key = (presupuesto_data.IdCliente, presupuesto_data.Anio, presupuesto_data.Mes)

    if key in _presupuestos_mock:
        raise HTTPException(status_code=400, detail="Ya existe presupuesto para este cliente, mes y año")
    
    if not (1 <= presupuesto_data.Mes <= 12):
        raise HTTPException(status_code=400, detail="Mes debe estar entre 1 y 12")

    id_presupuesto = len(_presupuestos_mock) + 1

    _presupuestos_mock[key] = {
        "IdPresupuesto": id_presupuesto,
        "IdCliente": presupuesto_data.IdCliente,
        "Anio": presupuesto_data.Anio,
        "Mes": presupuesto_data.Mes,
        "MontoLimite": presupuesto_data.MontoLimite,
        "FechaCreacion": datetime.now()
    }

    return PresupuestoResponse(**_presupuestos_mock[key])

def obtener_presupuesto_mensual(db, id_cliente: int, anio: int, mes: int) -> PresupuestoResponse:
    key = (id_cliente, anio, mes)

    if key not in _presupuestos_mock:
        raise HTTPException(status_code=404, detail="Presupuesto mensual no encontrado")

    return PresupuestoResponse(**_presupuestos_mock[key])

def listar_presupuestos_cliente(db, id_cliente: int) -> List[PresupuestoResponse]:
    cliente_presupuestos = [
        p for p in _presupuestos_mock.values()
        if p["IdCliente"] == id_cliente
    ]

    return [PresupuestoResponse(**p) for p in cliente_presupuestos]

def actualizar_presupuesto_mensual(db, id_presupuesto: int, update_data: PresupuestoUpdate) -> PresupuestoResponse:
    for data in _presupuestos_mock.values():
        if data["IdPresupuesto"] == id_presupuesto:
            if update_data.MontoLimite is not None:
                data["MontoLimite"] = update_data.MontoLimite

            data["FechaCreacion"] = datetime.now()
            return PresupuestoResponse(**data)

    raise HTTPException(status_code=404, detail="Presupuesto no encontrado")

def eliminar_presupuesto_mensual(db, id_presupuesto: int):
    for key, data in list(_presupuestos_mock.items()):
        if data["IdPresupuesto"] == id_presupuesto:
            del _presupuestos_mock[key]
            return {"mensaje": f"Presupuesto {id_presupuesto} eliminado exitosamente"}

    raise HTTPException(status_code=404, detail="Presupuesto no encontrado")