from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.gasto_recurrente_model import GastoRecurrente

router = APIRouter(
    prefix="/recurring-expenses",
    tags=["Gastos Recurrentes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/{id}")
def eliminar_gasto_recurrente(id: int, db: Session = Depends(get_db)):

    gasto = db.query(GastoRecurrente).filter(
        GastoRecurrente.IdGastoRecurrente == id
    ).first()

    if not gasto:
        raise HTTPException(
            status_code=404,
            detail="Gasto no encontrado"
        )

    gasto.Activo = False
    db.commit()

    return {
        "message": f"Gasto {id} eliminado correctamente"
    }