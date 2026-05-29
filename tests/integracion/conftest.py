import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from routes.ingreso_routes import get_db
import os
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_CadenaConection")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def fixture_db_session():
    """Crea una sesión de BD envuelta en una transacción que siempre hace rollback."""
    connection = engine.connect()
    # Iniciamos una transacción a nivel de conexión de SQLAlchemy
    transaction = connection.begin()
    
    # Vinculamos la sesión de ORM a esta conexión con la transacción activa
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        # Al terminar el test, revertimos TODO (incluso los db.commit() ejecutados dentro de tus servicios)
        transaction.rollback()
        connection.close()

@pytest.fixture(name="client")
def fixture_client(db_session):
    """Crea un TestClient de FastAPI que inyecta la sesión con Rollback activo."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # La limpieza real la hace el fixture db_session

    # Sobrescribimos la dependencia 'get_db' de tu router para que use nuestra sesión controlada
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    # Limpiamos las modificaciones de dependencias al finalizar los tests
    app.dependency_overrides.clear()