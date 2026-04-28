from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services.filtrado_service import filtrar_movimientos_por_mes

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/filtrar")
def filtrar(mes: int, anio: int, db: Session = Depends(get_db)):
    return filtrar_movimientos_por_mes(mes, anio, db)
