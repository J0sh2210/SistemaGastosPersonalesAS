from fastapi import FastAPI
from usuario.routes import router as usuario_router

app = FastAPI()

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])