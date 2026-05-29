from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_presupuesto_exitoso():
    with patch("routes.budget_routes.registrar_presupuesto") as mock_reg:
        with patch("routes.budget_routes.DataManager") as mock_dm:
            mock_reg.return_value = {"success": True, "message": "Presupuesto registrado: $500.0"}
            mock_dm.return_value.get_categories_data.return_value = []
            response = client.post("/presupuestos/", json={
                "user_id": 1,
                "month": "2026-05",
                "category": "Comida",
                "amount": 500.0
            })
            assert response.status_code == 200
            assert response.json()["success"] == True


def test_create_presupuesto_error_validacion():
    with patch("routes.budget_routes.registrar_presupuesto") as mock_reg:
        mock_reg.side_effect = ValueError("Categoria no existe")
        response = client.post("/presupuestos/", json={
            "user_id": 1,
            "month": "2026-05",
            "category": "Invalida",
            "amount": 500.0
        })
        assert response.status_code == 400


def test_get_presupuestos_exitoso():
    with patch("routes.budget_routes.DataManager") as mock_dm:
        mock_dm.return_value.get_categories_data.return_value = [
            {"categoria": "Comida", "monto": 500.0}
        ]
        response = client.get("/presupuestos/1/2026-05")
        assert response.status_code == 200
        assert "presupuestos" in response.json()
