from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crear_gasto_recurrente():

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
    assert response.json()["Concepto"] == "Netflix"


def test_listar_gastos_recurrentes():

    response = client.get(
        "/gastos-recurrentes/1"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_actualizar_gasto_recurrente():

    # Crear gasto primero
    crear_response = client.post(
        "/gastos-recurrentes/",
        json={
            "Concepto": "Netflix",
            "Monto": 250,
            "FechaInicio": "2026-05-28",
            "Frecuencia": "mensual",
            "IdCliente": 1
        }
    )

    assert crear_response.status_code == 200

    # Obtener el ID creado
    gasto_id = crear_response.json()["IdGastoRecurrente"]

    # Actualizar usando el ID real
    response = client.put(
        f"/gastos-recurrentes/{gasto_id}",
        json={
            "Concepto": "Netflix Premium",
            "Monto": 500,
            "Frecuencia": "mensual"
        }
    )

    assert response.status_code == 200
    assert response.json()["Concepto"] == "Netflix Premium"


def test_generar_gastos_mensuales():

    response = client.get(
        "/gastos-recurrentes/generate-monthly"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Gastos procesados"


def test_desactivar_gasto_recurrente():

    # Crear gasto primero
    crear_response = client.post(
        "/gastos-recurrentes/",
        json={
            "Concepto": "Spotify",
            "Monto": 100,
            "FechaInicio": "2026-05-28",
            "Frecuencia": "mensual",
            "IdCliente": 1
        }
    )

    assert crear_response.status_code == 200

    # Obtener ID real
    gasto_id = crear_response.json()["IdGastoRecurrente"]

    # Desactivar gasto
    response = client.put(
        f"/gastos-recurrentes/desactivar/{gasto_id}"
    )

    assert response.status_code == 200