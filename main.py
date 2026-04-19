from fastapi import FastAPI

from app.routes import router
#/*ELR_ENMA*/
# =============================
# CONFIGURACIÓN DE APP
# =============================

app = FastAPI(
    title="Gastos Recurrentes API",
    description="API para gestionar gastos recurrentes personales",
    version="1.0.0"
)

# =============================
# INCLUIR RUTAS
# =============================

app.include_router(router)

# =============================
# ENDPOINT RAÍZ
# =============================

@app.get("/", tags=["General"])
def read_root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a la API de Gastos Recurrentes",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

