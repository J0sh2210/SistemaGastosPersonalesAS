from fastapi import FastAPI, Depends

from database import SessionLocal
from routes.presupuesto_routes import router as presupuesto_router
from routes.categoria_routes import router as categoria_router
from routes.usuario_routes import router as usuario_router
from routes.movimiento_routes import router as movimiento_router
from routes.gasto_recurrente_routes import router as gastorecu_router
from routes.gasto_routes import router as gasto_router
from routes.ingreso_routes import router as ingreso_router
from routes.filtrado_routes import router as filtrado_router
from fastapi.middleware.cors import CORSMiddleware
from models.tipo_movimiento_model import TipoMovimiento
from models.movimiento_model import Movimiento


from routes.movimiento_routes import router as movimiento_router

app = FastAPI(title="Sistema de Gastos Personales API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # El "*" permite que cualquier página se conecte (ideal para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite POST, GET, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite cualquier encabezado
)

# =====================================
# RUTAS
# =====================================


# Permitir CORS para que el frontend pueda conectarse


app.include_router(categoria_router)
app.include_router(usuario_router, prefix="/usuarios")
app.include_router(movimiento_router, prefix="/movimientos", tags=["Movimientos"])
app.include_router(gasto_router, prefix="/gastos", tags=["Movimientos"])
app.include_router(gastorecu_router, prefix="/gastos-recurrentes", tags=["Gastos Recurrentes"])
app.include_router(ingreso_router)
app.include_router(presupuesto_router, prefix="/presupuestos", tags=["Presupuestos"])
app.include_router(filtrado_router, prefix="/movimientos", tags=["Filtrado"])
app.include_router(movimiento_router)


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
