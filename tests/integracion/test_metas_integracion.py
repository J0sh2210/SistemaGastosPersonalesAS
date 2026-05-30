import pytest
from datetime import date, timedelta

def test_integracion_crear_y_editar_meta(client):
    """Prueba la creación y edición de una meta de ahorro"""
    
    # --- PASO 1: Crear la meta ---
    payload_nuevo = {
        "id_usuario": 1,
        "nombre_meta": "Vacaciones de Verano",
        "monto_objetivo": 5000.00,
        "monto_actual": 0.00,
        "fecha_limite": str(date.today() + timedelta(days=60))
    }
    
    response_post = client.post("/api/metas/", json=payload_nuevo)
    assert response_post.status_code == 201
    
    # Validamos que devuelva un mensaje de éxito (ajusta el texto si tu API dice otra cosa)
    datos_post = response_post.json()
    assert "mensaje" in datos_post or "message" in datos_post # Valida que haya un mensaje de éxito

    # --- PASO 2: Buscar la meta por GET para obtener su ID ---
    response_get = client.get("/api/metas/1")
    assert response_get.status_code == 200
    lista_metas = response_get.json()
    meta_creada = next((m for m in lista_metas if m.get("NombreMeta") == "Vacaciones de Verano"), None)
    
    assert meta_creada is not None, "No se encontró la meta recién creada en el GET"
    # ¡CORRECCIÓN AQUÍ! Usamos "MontoObjetivo"
    assert float(meta_creada["MontoObjetivo"]) == 5000.00
    
    # ¡CORRECCIÓN AQUÍ! Usamos "IdMeta"
    id_meta = meta_creada["IdMeta"]

    # --- PASO 3: Editar la meta ---
    payload_editado = {
        "monto_actual": 1000.00
    }
    
    response_put = client.put(f"/api/metas/cantidad/{id_meta}", json=payload_editado)
    assert response_put.status_code == 200
    
    # Seguramente el PUT también devuelve un mensaje y no el objeto completo
    datos_put = response_put.json()
    assert "mensaje" in datos_put or "message" in datos_put


def test_integracion_listar_metas(client):
    """Prueba la obtención de la lista de metas de un usuario"""
    id_usuario = 1
    response = client.get(f"/api/metas/{id_usuario}")
    
    assert response.status_code == 200
    datos = response.json()
    assert isinstance(datos, list)