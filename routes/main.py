from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data_manager import DataManager
from datetime import datetime
from typing import Dict, Any

app = FastAPI(title="Alerta de Presupuesto API")

dm = DataManager()

class BudgetItem(BaseModel):
    month: str
    category: str
    amount: float

class ThresholdItem(BaseModel):
    threshold: float

@app.get("/")
def root():
    return {"message": "Alerta de Presupuesto API. Visita /docs para interactuar."}

@app.get("/current-month")
def current_month():
    return {"month": dm.get_current_month()}

@app.get("/categories/{month}")
def get_categories(month: str) -> Dict[str, Any]:
    data = dm.get_categories_data(month)
    if not data:
        raise HTTPException(status_code=404, detail="No budgets found for month")
    return {"month": month, "categories": data}

@app.post("/budgets/")
def add_budget(item: BudgetItem):
    dm.add_budget(item.month, item.category, item.amount)
    return {"message": f"Presupuesto agregado: {item.category} - ${item.amount} para {item.month}"}

@app.post("/expenses/")
def add_expense(item: BudgetItem):
    dm.add_budget(item.month, item.category, 0)  # Ensure budget exists
    alert_triggered = dm.add_expense(item.month, item.category, item.amount)
    alert_msg = "¡Alerta! " if alert_triggered else ""
    alert_msg += f"Gasto agregado: {item.category} - ${item.amount} en {item.month}"
    if alert_triggered:
        categories = dm.get_categories_data(item.month)
        cat_data = categories.get(item.category, {})
        alert_msg += f"\nCategoría {item.category}: {cat_data.get('spent', 0):.2f}/{cat_data.get('budgeted', 0):.2f} ({cat_data.get('percentage', 0)}%) - {cat_data.get('status', 'unknown')}"
    return {"message": alert_msg}

@app.get("/config/threshold")
def get_threshold():
    return {"threshold": dm.get_threshold()}

@app.put("/config/threshold")
def set_threshold(item: ThresholdItem):
    if not 0 < item.threshold < 100:
        raise HTTPException(status_code=400, detail="Threshold must be between 0 and 100")
    dm.set_threshold(item.threshold)
    return {"message": f"Umbral actualizado a {item.threshold}%"}

@app.post("/reset")
def reset():
    dm.reset_data()
    return {"message": "Datos de gastos y alertas reiniciados"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
