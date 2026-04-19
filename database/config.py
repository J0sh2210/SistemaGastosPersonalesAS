from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#/*ELR_ENMA*/

# =============================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================
DATABASE_URL = (
    "mssql+pyodbc://@ENMITA\\SQLEXPRESS/SistemasGastosAS"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Crear todas las tablas
Base.metadata.create_all(bind=engine)
