from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from services.budget_service import registrar_presupuesto
from models.data_manager import DataManager

router = APIRouter(prefix='/presupuestos', tags=['Presupuestos'])

class PresupuestoCreate(BaseModel):
    user_id: int = 1
    month: str
    category: Optional[str] = None  # Optional -> 'General'
    amount: float

@router.post('/')
def create_presupuesto(item: PresupuestoCreate):
    """
    Registrar Presupuesto Mensual
    Valida user_id y category (o 'General'), guarda/actualiza en DB.
    Ejemplo: {"user_id": 1, "month": "2024-12", "category": "Comida", "amount": 500.0}
    """
    try:
        result = registrar_presupuesto(item.user_id, item.month, item.category, item.amount)
        dm = DataManager()
        categories = dm.get_categories_data(item.month, item.user_id)
        return {'success': True, 'message': result['message'], 'presupuestos': categories}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@router.get('/{user_id}/{month}')
def get_presupuestos(user_id: int, month: str):
    """
    Consultar Presupuestos
    Lista presupuestos y % gastado por mes/user.
    """
    dm = DataManager()
    categories = dm.get_categories_data(month, user_id)
    return {'mes': month, 'presupuestos': categories}
