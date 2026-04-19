from typing import Generator

from sqlalchemy.orm import Session

from database.config import SessionLocal

# =============================
# DEPENDENCIAS
# =============================

def get_db() -> Generator[Session, None, None]:
    """Dependencia para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
