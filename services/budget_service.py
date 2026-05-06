from database.db_manager import get_db, sp_registrar_presupuesto
from typing import Optional

def registrar_presupuesto(user_id: int, month: str, category: str, amount: float) -> dict:
    """
    Registra/actualiza presupuesto mensual via SP func.
    Valida: user_id exists, category exists or 'General'.
    """
    from database.db_manager import sp_registrar_presupuesto
    sp_registrar_presupuesto(user_id, month, category or 'General', amount)
    return {'success': True, 'message': f"Presupuesto {category or 'General'} registrado: ${amount}"}
