from http import client
import pytest

def test_integracion_crear_y_editar_categoria(client):
    """Prueba la creación y edición de una categoría"""
    
    # --- PASO 1: Crear una nueva categoría ---
    payload_nuevo = {
        "nombre_categoria": "Transporte",
        "id_tipo_movimiento": 2,
        "id_tipo_categoria": 1
    }
    
    response_post = client.post("/categorias/", json=payload_nuevo)
    assert response_post.status_code == 200
    assert response_post.json()["mensaje"] == "Categoría creada correctamente"

    # --- PASO 2: Buscar la categoría creada para obtener su ID ---
    response_get = client.get("/categorias/")
    assert response_get.status_code == 200
    lista_categorias = response_get.json()
    
    # ¡CORRECCIÓN AQUÍ! Usamos "nombre" e "id"
    categoria_creada = next((cat for cat in lista_categorias if cat["nombre"] == "Transporte"), None)
    
    assert categoria_creada is not None, "No se encontró la categoría recién creada"
    IdCategoria = categoria_creada["id"]

    # --- PASO 3: Editar la categoría ---
    payload_editado = {
        "nombre_categoria": "Transporte y Movilidad",
        "id_tipo_movimiento": 2,
        "id_tipo_categoria": 1
    }
    
    response_put = client.put(f"/categorias/{IdCategoria}", json=payload_editado)
    assert response_put.status_code == 200
    
    # ¡CORRECCIÓN AQUÍ! El PUT devuelve un mensaje, no el objeto editado
    assert response_put.json()["mensaje"] == "Categoría actualizada correctamente"


def test_integracion_listar_categorias(client):
    """Prueba la obtención de la lista de categorías"""
    response = client.get("/categorias/")
    
    assert response.status_code == 200
    datos = response.json()
    assert isinstance(datos, list)


def test_integracion_eliminar_categoria(client):
    """Prueba la creación y eliminación de una categoría"""
    
    # --- PASO 1: Crear una categoría ---
    payload = {
        "nombre_categoria": "Categoría Temporal",
        "id_tipo_movimiento": 2,
        "id_tipo_categoria": 1
    }
    
    response_post = client.post("/categorias/", json=payload)
    assert response_post.status_code == 200
    assert response_post.json()["mensaje"] == "Categoría creada correctamente"
    
    # --- PASO 2: Obtener el ID buscándola en la lista ---
    lista_categorias = client.get("/categorias/").json()
    
    # ¡CORRECCIÓN AQUÍ! Usamos "nombre" e "id"
    categoria_temporal = next((cat for cat in lista_categorias if cat["nombre"] == "Categoría Temporal"), None)
    
    assert categoria_temporal is not None, "No se encontró la categoría temporal"
    IdCategoria = categoria_temporal["id"]
    
    # --- PASO 3: Eliminar la categoría ---
    response_delete = client.delete(f"/categorias/{IdCategoria}")
    assert response_delete.status_code == 200
    assert response_delete.json()["mensaje"] == "Categoría eliminada correctamente"