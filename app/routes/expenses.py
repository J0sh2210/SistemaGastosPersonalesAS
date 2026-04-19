from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import RecurringExpense
#/*ELR_ENMA*/

router = APIRouter(prefix="/expenses", tags=["expenses"])
#/*ELR_ENMA*/



# /*GENERAR GASTOS MENSUALES*/

@router.get("/generate-monthly", summary="Generar gastos mensuales automáticamente")
def generate_monthly_expenses(db: Session = Depends(get_db)):
    """
    Genera todos los gastos recurrentes activos para el mes actual.
    """
    today = date.today()
    expenses = db.query(RecurringExpense).filter(
        RecurringExpense.is_active == True
    ).all()

    generated = []
    for exp in expenses:
        if exp.FechaInicio.day == today.day:
            generated.append({
                "Concepto": exp.Concepto,
                "Monto": float(exp.Monto),
                "Fecha": today
            })

    return {
        "message": "Gastos generados",
        "data": generated
    }
