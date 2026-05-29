from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_categoria():
    with patch("routes.categoria_routes.crear_categoria") as mock:
        mock.return_value = {"mensaje": "Categoria creada correctamente"}
        response = client.post("/categorias/", json={
            "nombre_categoria": "Comida",
            "id_tipo_movimiento": 1,
            "id_tipo_categoria": 2
        })
        assert response.status_code == 200

def test_obtener_categorias():
    with patch("routes.categoria_routes.obtener_categorias") as mock:
        mock.return_value = [{"id": 1, "nombre": "Comida"}]
        response = client.get("/categorias/")
        assert response.status_code == 200

def test_editar_categoria():
    with patch("routes.categoria_routes.editar_categoria") as mock:
        mock.return_value = {"mensaje": "Actualizado"}
        response = client.put("/categorias/1", json={"nombre_categoria": "Transporte"})
        assert response.status_code == 200

def test_eliminar_categoria():
    with patch("routes.categoria_routes.eliminar_categoria") as mock:
        mock.return_value = {"mensaje": "Eliminado"}
        response = client.delete("/categorias/1")
        assert response.status_code == 200