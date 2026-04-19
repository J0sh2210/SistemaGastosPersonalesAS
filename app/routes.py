from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import RecurringExpense
from app.schemas import RecurringExpenseCreate, RecurringExpenseRead, RecurringExpenseUpdate

# =============================
# ROUTER
# =============================

router = APIRouter(
    prefix="/recurring-expenses",
    tags=["Gastos Recurrentes"]
)

# =============================
# CREAR
# =============================

@router.post("", response_model=RecurringExpenseRead, summary="Crear gasto recurrente")
def create_recurring_expense(
    expense: RecurringExpenseCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo gasto recurrente"""
    db_obj = RecurringExpense(
        Concepto=expense.Concepto,
        Monto=expense.Monto,
        FechaInicio=expense.FechaInicio,
        Frecuencia=expense.Frecuencia.value,
        IdCliente=expense.IdCliente,
        is_active=True
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


# =============================
# LISTAR
# =============================

@router.get("", response_model=List[RecurringExpenseRead], summary="Listar gastos recurrentes")
def list_recurring_expenses(db: Session = Depends(get_db)):
    """Listar todos los gastos recurrentes"""
    return db.query(RecurringExpense).all()


# =============================
# OBTENER POR ID
# =============================

@router.get("/{id}", response_model=RecurringExpenseRead, summary="Obtener gasto por ID")
def get_recurring_expense(id: int, db: Session = Depends(get_db)):
    """Obtener un gasto recurrente por su ID"""
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return expense


# =============================
# ACTUALIZAR
# =============================

@router.put("/{id}", response_model=RecurringExpenseRead, summary="Actualizar gasto recurrente")
def update_recurring_expense(
    id: int,
    expense_update: RecurringExpenseUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un gasto recurrente"""
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    update_data = expense_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "Frecuencia":
            value = value.value
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


# =============================
# ELIMINAR
# =============================

@router.delete("/{id}", summary="Eliminar gasto recurrente")
def delete_recurring_expense(id: int, db: Session = Depends(get_db)):
    """Eliminar un gasto recurrente"""
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    db.delete(expense)
    db.commit()

    return {"message": "Eliminado correctamente"}


# =============================
# ACTIVAR / DESACTIVAR
# =============================

@router.put("/{id}/toggle", summary="Activar o desactivar gasto")
def toggle_expense(id: int, db: Session = Depends(get_db)):
    """Activar o desactivar un gasto recurrente"""
    expense = db.query(RecurringExpense).filter(
        RecurringExpense.IdGastoRecurrente == id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    expense.is_active = not expense.is_active
    db.commit()

    return {"message": "Estado actualizado", "is_active": expense.is_active}
