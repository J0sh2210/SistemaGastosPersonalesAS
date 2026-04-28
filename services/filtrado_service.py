from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException


def filtrar_movimientos_por_mes(mes: int, anio: int, db: Session):
    if mes < 1 or mes > 12:
        raise HTTPException(status_code=400, detail="El mes debe estar entre 1 y 12")
    if anio < 2000:
        raise HTTPException(status_code=400, detail="El anio no es valido")

    result = db.execute(text("""
        EXEC sp_FiltrarMovimientosPorMes
            @Mes  = :mes,
            @Anio = :anio
    """), {
        "mes": mes,
        "anio": anio
    }).fetchall()

    return [row._mapping for row in result]
