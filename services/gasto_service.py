from sqlalchemy.orm import Session
from models.movimiento_model import Movimiento
from models.schemas import GastoCreate
from fastapi import HTTPException

ID_TIPO_GASTO = 2 # Según tu script SQL (Egreso)

def obtener_gastos(db: Session):
    return db.query(Movimiento).filter(Movimiento.IdTipo == ID_TIPO_GASTO).all()

def crear_nuevo_gasto(db: Session, gasto_data: GastoCreate):
    nuevo_gasto = Movimiento(
        Concepto=gasto_data.Concepto,
        Monto=gasto_data.Monto,
        IdCliente=gasto_data.IdCliente,
        IdCategoria=gasto_data.IdCategoria,
        IdTipo=ID_TIPO_GASTO
    )
    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)
    return nuevo_gasto

def eliminar_gasto_db(db: Session, id_gasto: int):
    gasto = db.query(Movimiento).filter(Movimiento.IdMovimiento == id_gasto, Movimiento.IdTipo == ID_TIPO_GASTO).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    db.delete(gasto)
    db.commit()
    return {"mensaje": "Gasto eliminado exitosamente"}

def actualizar_gasto_db(db: Session, id_gasto: int, datos: GastoCreate):
    gasto = db.query(Movimiento).filter(Movimiento.IdMovimiento == id_gasto, Movimiento.IdTipo == ID_TIPO_GASTO).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    gasto.Concepto = datos.Concepto
    gasto.Monto = datos.Monto
    gasto.IdCliente = datos.IdCliente
    gasto.IdCategoria = datos.IdCategoria
    
    db.commit()
    db.refresh(gasto)
    return gasto