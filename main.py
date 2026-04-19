from fastapi import FastAPI

from app.database import Base, engine
from app.routes.expenses import router as expenses_router
#/*ELR_ENMA*/

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(title="Generar Gastos Mensuales")

# Incluir rutas
app.include_router(expenses_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )