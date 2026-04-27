from fastapi import FastAPI

from database import SessionLocal
from routes.categoria_routes import router as categoria_router
from routes.usuario_routes import router as usuario_router
from routes.movimiento_routes import router as movimiento_router
from routes.gasto_recurrente_routes import router as gasto_router

app = FastAPI(title="Sistema de Gastos Personales API")

# =====================================
# RUTAS
# =====================================
app.include_router(categoria_router)
app.include_router(usuario_router, prefix="/usuarios")
app.include_router(movimiento_router, prefix="/movimientos", tags=["Movimientos"])
app.include_router(gasto_router)

# =====================================
# SESION BD
# =====================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================
# INICIO
# =====================================
@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gastos Personales API"}