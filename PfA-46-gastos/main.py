from fastapi import FastAPI
from sqlalchemy import text

from database import engine
from routes.gasto_routes import router as gasto_router

app = FastAPI(title="PfA-46 — Registro y Edición de Gastos API")

app.include_router(gasto_router)

@app.get("/")
def read_root():
    return {"message": "PfA-46 API de Gastos"}

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

