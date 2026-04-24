from fastapi import APIRouter, HTTPException
from typing import List
from registro.alerta.models.alert_model import AlertCreate, AlertUpdate, AlertResponse
from registro.alerta.services.alert_service import create_alert, update_alert, delete_alert
from models.data_manager import DataManager

router = APIRouter(prefix="/alertas", tags=["alertas"])

dm = DataManager()

@router.post("/", response_model=dict)
def register_alert(alert_data: AlertCreate):
    try:
        alert_id = create_alert(dm, alert_data)
        return {"message": "Alerta registrada", "id": alert_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{alert_id}", response_model=dict)
def modify_alert(alert_id: str, update_data: AlertUpdate):
    try:
        updated = update_alert(dm, alert_id, update_data)
        return {"message": "Alerta modificada", "updated": updated}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{alert_id}")
def remove_alert(alert_id: str):
    try:
        delete_alert(dm, alert_id)
        return {"message": "Alerta eliminada"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{month}", response_model=List[AlertResponse])
def get_alerts_month(month: str):
    alerts = dm.get_alerts_data(month)
    return [AlertResponse(**alert) for alert in alerts]

