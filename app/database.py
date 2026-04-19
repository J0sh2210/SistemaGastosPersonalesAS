from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
#/*ELR_ENMA*/

# =============================
# CONEXIÓN A BASE DE DATOS
# =============================
DATABASE_URL = (
    "mssql+pyodbc://@ENMITA\\SQLEXPRESS/SistemasGastosAS"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
