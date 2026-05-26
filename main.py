from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal

# Importaciones de routers
from routes.presupuesto_routes import router as presupuesto_router
from routes.categoria_routes import router as categoria_router
from routes.usuario_routes import router as usuario_router
from routes.movimiento_routes import router as movimiento_router
from routes.gasto_recurrente_routes import router as gastorecu_router
from routes.gasto_routes import router as gasto_router
from routes.ingreso_routes import router as ingreso_router
from routes.filtrado_routes import router as filtrado_router
from routes.meta_routes import router as meta_router

app = FastAPI(title="Sistema de Gastos Personales API")

# =====================================
# CONFIGURACIÓN DE CORS
# =====================================
origenes_permitidos = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos, # <-- CORREGIDO: Cambiado "*" por la lista explícita
    allow_credentials=True,            # <-- Requerido para poder enviar el Token Bearer
    allow_methods=["*"],               # Permite POST, GET, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],               # Permite todos los encabezados de autenticación
)

# =====================================
# INCLUSIÓN DE ROUTERS (RUTAS)
# =====================================
app.include_router(categoria_router)
app.include_router(usuario_router, prefix="/usuarios")
app.include_router(movimiento_router, prefix="/movimientos", tags=["Movimientos"])
app.include_router(gasto_router, prefix="/gastos", tags=["Movimientos"])
app.include_router(gastorecu_router, prefix="/gastos-recurrentes", tags=["Gastos Recurrentes"])
app.include_router(ingreso_router)
app.include_router(presupuesto_router)
app.include_router(filtrado_router, prefix="/movimientos", tags=["Filtrado"])
app.include_router(meta_router)


# Dependencia de la Base de Datos
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