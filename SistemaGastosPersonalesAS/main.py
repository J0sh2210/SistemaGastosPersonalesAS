from fastapi import FastAPI

from SistemaGastosPersonalesAS.database import SessionLocal
from SistemaGastosPersonalesAS.routes.categoria_routes import router as categoria_router

app = FastAPI(tittle="Sistema de Gastos Personales API")
app.include_router(categoria_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gastos Personales API"}