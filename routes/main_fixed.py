from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from pydantic import BaseModel
from models.data_manager import DataManager
from typing import Dict, Any, List
from datetime import datetime
from registro.alerta.routes.alert_routes import router as alert_router

app = FastAPI(
    title="Alerta de Presupuesto API",
    description="API para gestión de presupuestos con alertas automáticas (80% y 100%).",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dm = DataManager()

app.include_router(alert_router)


class BudgetItem(BaseModel):
    month: str
    category: str
    amount: float

class ThresholdItem(BaseModel):
    threshold: float

@app.get("/")
def root():
    return {"message": "Alerta de Presupuesto API v1.0. Visita /docs para Swagger UI."}

@app.get("/current-month")
def current_month():
    return {"month": dm.get_current_month()}

@app.get("/categories/{month}")
def get_categories(month: str) -> Dict[str, Any]:
    """Obtiene datos de categorías para mes: % gasto, status para highlights/progreso."""
    data = dm.get_categories_data(month)
    if not data:
        raise HTTPException(status_code=404, detail="No budgets found for this month")
    return {
        "month": month,
        "categories": data,
        "summary": {
            "total_budgeted": sum(cat["budgeted"] for cat in data.values()),
            "total_spent": sum(cat["spent"] for cat in data.values()),
            "overall_percentage": round(
                (sum(cat["spent"] for cat in data.values()) / sum(cat["budgeted"] for cat in data.values()) * 100)
                if sum(cat["budgeted"] for cat in data.values()) > 0 else 0, 2
            )
        }
    }

@app.post("/budgets/")
def add_budget(item: BudgetItem):
    dm.add_budget(item.month, item.category, item.amount)
    return {
        "message": f"Presupuesto agregado/actualizado: {item.category} - ${item.amount:.2f} para {item.month}",
        "categories": dm.get_categories_data(item.month)
    }

@app.post("/expenses/")
def add_expense(item: BudgetItem):
    # Ensure budget exists
    if not dm.budget_exists(item.month, item.category):
        raise HTTPException(status_code=400, detail="Budget not found for category. Add budget first.")
    
    alert_triggered = dm.add_expense(item.month, item.category, item.amount)
    categories = dm.get_categories_data(item.month)
    cat_data = categories[item.category]
    
    msg = f"Gasto agregado: {item.category} - ${item.amount:.2f}"
    if alert_triggered or cat_data["status"] in ["warning", "exceeded"]:
        status = cat_data["status"]
        msg = f"🚨 ALERTA {status.upper()}! Categoría: {item.category}, Gastado: ${cat_data['spent']:.2f} / Presupuesto: ${cat_data['budgeted']:.2f} ({cat_data['percentage']}%)"
    
    return {
        "message": msg,
        "updated_category": cat_data,
        "categories": categories
    }

@app.get("/alerts/{month}")
def get_alerts(month: str) -> Dict[str, Any]:
    """Lista alertas nuevas (no vistas) para el mes: categoría, % , status."""
    alerts = dm.get_new_alerts(month)
    result = []
    for alert in alerts:
        result.append({
            "id": alert["id"],
            "category": alert["category"],
            "spent": alert["spent"],
            "budgeted": alert["budgeted"],
            "percentage": alert["percentage"],
            "status": alert["status"]
        })
        dm.mark_alert_seen(month, alert["category"])
    return {"month": month, "new_alerts": result}

@app.get("/config/threshold")
def get_threshold():
    return {"threshold": dm.get_threshold()}

@app.put("/config/threshold")
def set_threshold(item: ThresholdItem):
    if not 0 < item.threshold < 100:
        raise HTTPException(status_code=400, detail="Threshold must be between 0 and 100")
    dm.set_threshold(item.threshold)
    return {"message": f"Umbral de alerta actualizado a {item.threshold}%", "new_threshold": item.threshold}

@app.post("/reset")
def reset_data():
    dm.reset_data()
    return {"message": "Gastos y alertas reiniciados para todos los meses."}

@app.get("/docs")
def docs_redirect():
    return {"docs": "Go to /docs for interactive API."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
