from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crear_presupuesto_mes_actual():
    from datetime import datetime
    mes_actual = datetime.now().strftime("%Y-%m")
    with patch("routes.presupuesto_routes.crear_presupuesto_mensual") as mock_crear:
        mock_crear.return_value = {"mensaje": "Presupuesto creado correctamente"}
        response = client.post("/presupuestos/", json={
            "monto_presupuesto": 1000.0,
            "id_categoria": 1,
            "mes_aplicacion": mes_actual,
            "id_usuario": 1
        })
        assert response.status_code == 200


def test_crear_presupuesto_mes_incorrecto():
    response = client.post("/presupuestos/", json={
        "monto_presupuesto": 1000.0,
        "id_categoria": 1,
        "mes_aplicacion": "2020-01",
        "id_usuario": 1
    })
    assert response.status_code == 400
    assert "mes actual" in response.json()["detail"]


def test_listar_presupuestos():
    with patch("routes.presupuesto_routes.obtener_presupuestos") as mock_obtener:
        mock_obtener.return_value = []
        response = client.get("/presupuestos/")
        assert response.status_code == 200


def test_editar_presupuesto():
    with patch("routes.presupuesto_routes.actualizar_presupuesto") as mock_actualizar:
        mock_actualizar.return_value = {"mensaje": "Presupuesto actualizado"}
        response = client.put("/presupuestos/1", json={
            "monto_presupuesto": 2000.0
        })
        assert response.status_code == 200


def test_eliminar_presupuesto():
    with patch("routes.presupuesto_routes.eliminar_presupuesto") as mock_eliminar:
        mock_eliminar.return_value = {"mensaje": "Presupuesto eliminado correctamente"}
        response = client.delete("/presupuestos/1")
        assert response.status_code == 200
