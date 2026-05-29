from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app

client = TestClient(app)

# Creamos una función auxiliar para configurar nuestra DB falsa
# Creamos una función auxiliar para configurar nuestra DB falsa
def configurar_mock_db(mock_session_local):
    mock_db = mock_session_local.return_value
    
    # 1. Simulamos db.query().filter().all() para que devuelva una lista vacía
    mock_db.query.return_value.filter.return_value.all.return_value = []
    
    # 2. Simulamos db.query().filter().first() para que devuelva un gasto válido
    mock_gasto = MagicMock()
    mock_gasto.IdGastoRecurrente = 1  # <- Clave para que el PUT no falle
    mock_gasto.Activo = True
    mock_gasto.Concepto = "Netflix"
    mock_gasto.Monto = 250.0
    mock_gasto.Frecuencia = "mensual"
    mock_db.query.return_value.filter.return_value.first.return_value = mock_gasto
    
    # 3. EL TRUCO MÁGICO PARA EL POST:
    # Cuando FastAPI haga db.refresh(nuevo_gasto), le asignamos un ID falso.
    def fake_refresh(obj):
        obj.IdGastoRecurrente = 1
        
    mock_db.refresh.side_effect = fake_refresh
    
    return mock_db

# --- PRUEBAS ---

# Interceptamos SessionLocal directamente en el archivo de rutas
@patch("routes.gasto_recurrente_routes.SessionLocal")
def test_crear_gasto_recurrente(mock_session_local):
    configurar_mock_db(mock_session_local)
    
    response = client.post(
        "/gastos-recurrentes/",
        json={
            "Concepto": "Netflix",
            "Monto": 250,
            "FechaInicio": "2026-05-28",
            "Frecuencia": "mensual",
            "IdCliente": 1
        }
    )
    assert response.status_code == 200


@patch("routes.gasto_recurrente_routes.SessionLocal")
def test_listar_gastos_recurrentes(mock_session_local):
    configurar_mock_db(mock_session_local)
    
    response = client.get("/gastos-recurrentes/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("routes.gasto_recurrente_routes.SessionLocal")
def test_actualizar_gasto_recurrente(mock_session_local):
    configurar_mock_db(mock_session_local)
    gasto_id = 1 

    response = client.put(
        f"/gastos-recurrentes/{gasto_id}",
        json={
            "Concepto": "Netflix Premium",
            "Monto": 500,
            "Frecuencia": "mensual"
        }
    )
    assert response.status_code == 200


@patch("routes.gasto_recurrente_routes.SessionLocal")
def test_generar_gastos_mensuales(mock_session_local):
    configurar_mock_db(mock_session_local)
    
    response = client.get("/gastos-recurrentes/generate-monthly")
    assert response.status_code == 200


@patch("routes.gasto_recurrente_routes.SessionLocal")
def test_desactivar_gasto_recurrente(mock_session_local):
    configurar_mock_db(mock_session_local)
    gasto_id = 1 
    
    response = client.put(f"/gastos-recurrentes/desactivar/{gasto_id}")
    assert response.status_code in [200, 204]