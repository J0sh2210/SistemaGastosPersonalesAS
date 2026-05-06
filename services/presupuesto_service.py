from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from models.presupuesto_model import Presupuesto # Solo para type hints, no usado en mocks
from models.schemas import PresupuestoCreate, PresupuestoUpdate, PresupuestoResponse

def crear_presupuesto_mensual(db: Session, presupuesto_data: PresupuestoCreate) -> PresupuestoResponse:
    # MOCK: Simulación sin BD para compilación (PFA-108 backend-only)
    # TODO: Descomentar cuando tabla 'presupuesto' exista
    """
    nuevo_presupuesto = Presupuesto(
        IdCliente=presupuesto_data.IdCliente,
        Anio=presupuesto_data.Anio,
        Mes=presupuesto_data.Mes,
        MontoPresupuestado=presupuesto_data.MontoPresupuestado
    )
    db.add(nuevo_presupuesto)
    db.commit()
    db.refresh(nuevo_presupuesto)
    return nuevo_presupuesto
    """
    from datetime import datetime
    return PresupuestoResponse(
        IdPresupuesto=1,
        IdCliente=presupuesto_data.IdCliente,
        Anio=presupuesto_data.Anio,
        Mes=presupuesto_data.Mes,
        MontoPresupuestado=presupuesto_data.MontoPresupuestado,
        FechaCreacion=datetime.now()
    )

def obtener_presupuesto_mensual(db: Session, id_cliente: int, anio: int, mes: int) -> PresupuestoResponse:
    # MOCK: Simulación sin BD (PFA-108)
    from datetime import datetime
    return PresupuestoResponse(
        IdPresupuesto=1,
        IdCliente=id_cliente,
        Anio=anio,
        Mes=mes,
        MontoPresupuestado=5000.0,
        FechaCreacion=datetime.now()
    )

def listar_presupuestos_cliente(db: Session, id_cliente: int) -> List[PresupuestoResponse]:
    # MOCK: Simulación sin BD (PFA-108)
    from datetime import datetime
    mock_presupuestos = [
        PresupuestoResponse(
            IdPresupuesto=1,
            IdCliente=id_cliente,
            Anio=2024,
            Mes=1,
            MontoPresupuestado=5000.0,
            FechaCreacion=datetime.now()
        )
    ]
    return mock_presupuestos

def actualizar_presupuesto_mensual(db: Session, id_presupuesto: int, update_data: PresupuestoUpdate) -> PresupuestoResponse:
    # MOCK: Simulación sin BD (PFA-108)
    from datetime import datetime
    return PresupuestoResponse(
        IdPresupuesto=id_presupuesto,
        IdCliente=1,
        Anio=2024,
        Mes=1,
        MontoPresupuestado=update_data.MontoPresupuestado if update_data.MontoPresupuestado else 6000.0,
        FechaCreacion=datetime.now()
    )

def eliminar_presupuesto_mensual(db: Session, id_presupuesto: int):
    # MOCK: Simulación sin BD (PFA-108)
    return {"mensaje": f"Presupuesto {id_presupuesto} eliminado exitosamente (simulado)"}

# TODO: Implementar CRUD real cuando tabla 'presupuesto' exista en BD
