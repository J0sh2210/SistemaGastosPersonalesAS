import json
from datetime import datetime
from models.data_manager import DataManager
from registro.alerta.models.alert_model import AlertCreate, AlertUpdate

def create_alert(dm: DataManager, alert_data: AlertCreate) -> str:
    # Generate ID: month_category_timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    alert_id = f"{alert_data.month}_{alert_data.category}_{timestamp}"
    
    # Prevent duplicate this month/category if already alert exists
    existing_month_cat = dm.get_alerts_by_month_category(alert_data.month, alert_data.category)
    if existing_month_cat:
        raise ValueError("Alert already exists for this month/category")
    
    dm.create_alert(alert_id, {
        "month": alert_data.month,
        "category": alert_data.category,
        "spent": alert_data.spent,
        "budgeted": alert_data.budgeted,
        "percentage": alert_data.percentage,
        "status": alert_data.status,
        "created_at": datetime.now().isoformat()
    })
    return alert_id

def update_alert(dm: DataManager, alert_id: str, update_data: AlertUpdate):
    alert = dm.get_alert(alert_id)
    if not alert:
        raise ValueError("Alert not found")
    
    updated = {**alert, **update_data.dict(exclude_unset=True)}
    dm.update_alert(alert_id, updated)
    return updated

def delete_alert(dm: DataManager, alert_id: str):
    if not dm.get_alert(alert_id):
        raise ValueError("Alert not found")
    dm.delete_alert(alert_id)


