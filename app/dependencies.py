from typing import Generator
from sqlalchemy.orm import Session

from app.database import SessionLocal
#/*ELR_ENMA*/


# =============================
# DEPENDENCIAS DE BASE DE DATOS
# =============================
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
