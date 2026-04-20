from fastapi import FastAPI

from database import SessionLocal
from routes.categoria_routes import router as categoria_router
from routes.usuario_routes import router as usuario_router

app = FastAPI(title="Sistema de Gastos Personales API")

app.include_router(categoria_router)
app.include_router(usuario_router, prefix="/usuarios")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gastos Personales API"}
