from fastapi import FastAPI

from SistemaGastosPersonalesAS.database import SessionLocal
app = FastAPI(tittle="Sistema de Gastos Personales API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gastos Personales API"}