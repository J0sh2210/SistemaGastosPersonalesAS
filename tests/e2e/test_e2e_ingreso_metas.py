import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from main import app  # Importa tu app de FastAPI

client = TestClient(app)

def test_e2e_flujo_completo_finanzas_usuario():
    """
    Prueba End-to-End simulando un flujo real de usuario:
    1. Crea una nueva categoría de ingresos.
    2. Registra un ingreso usando esa categoría.
    3. Crea una meta de ahorro con parte de ese dinero.
    4. Consulta la meta para validar que exista.
    5. Elimina la meta (Limpieza de DB).
    """
    # --- LIMPIEZA DE INTERFERENCIAS ---
    # Esto remueve cualquier Mock residual que otras pruebas unitarias
    # hayan dejado activo en el diccionario de dependencias de FastAPI
    app.dependency_overrides.clear()
    
    # --- DATOS GLOBALES PARA EL TEST ---
    id_usuario = 1
    nombre_categoria_e2e = "Ingresos Extra E2E"
    nombre_meta_e2e = "Laptop Nueva E2E"

    # ==========================================
    # PASO 1: CREAR UNA NUEVA CATEGORÍA
    # ==========================================
    payload_categoria = {
        "nombre_categoria": nombre_categoria_e2e,
        "id_tipo_movimiento": 1, 
        "id_tipo_categoria": 1
    }
    response_cat = client.post("/categorias/", json=payload_categoria)
    assert response_cat.status_code in [200, 201], "Fallo al crear la categoría"

    # ==========================================
    # PASO 2: OBTENER EL ID DE LA CATEGORÍA
    # ==========================================
    response_get_cats = client.get("/categorias/")
    assert response_get_cats.status_code == 200
    
    lista_categorias = response_get_cats.json()
    categoria_creada = next((c for c in lista_categorias if c.get("nombre") == nombre_categoria_e2e), None)
    
    assert categoria_creada is not None, "La categoría no se encontró tras crearla"
    id_cat_generado = categoria_creada["id"]

    # ==========================================
    # PASO 3: REGISTRAR UN INGRESO
    # ==========================================
    payload_ingreso = {
        "Concepto": "Pago Proyecto Freelance",
        "Monto": 2500.00,
        "IdCliente": id_usuario,
        "IdMovimiento": 999888, 
        "IdCategoria": id_cat_generado, 
        "IdTipo": 1
    }
    
    # Tu endpoint en ingreso_routes.py está en prefix="/ingresos"
    response_ingreso = client.post("/ingresos/", json=payload_ingreso)
    
    # Si devuelve 404 por la barra inclinada final, reintentamos sin ella
    if response_ingreso.status_code == 404:
        response_ingreso = client.post("/ingresos", json=payload_ingreso)
        
    assert response_ingreso.status_code in [200, 201], f"Fallo al registrar el ingreso. Respuesta: {response_ingreso.text}"
    
    # ==========================================
    # PASO 4: CREAR UNA META DE AHORRO
    # ==========================================
    payload_meta = {
        "id_usuario": id_usuario,
        "nombre_meta": nombre_meta_e2e,
        "monto_objetivo": 1000.00,
        "monto_actual": 500.00, 
        "fecha_limite": str(date.today() + timedelta(days=90))
    }
    
    # Probamos con y sin el prefijo /api/ por si el router maneja rutas puras
    response_meta = client.post("/api/metas/", json=payload_meta)
    if response_meta.status_code == 404:
        response_meta = client.post("/metas/", json=payload_meta)
    if response_meta.status_code == 404:
        response_meta = client.post("/metas", json=payload_meta)
        
    assert response_meta.status_code in [200, 201], f"Fallo al crear la meta de ahorro. Respuesta: {response_meta.text}"

    # ==========================================
    # PASO 5: VALIDAR LA META EN EL PERFIL (GET)
    # ==========================================
    response_get_metas = client.get(f"/api/metas/{id_usuario}")
    if response_get_metas.status_code == 404:
        response_get_metas = client.get(f"/metas/{id_usuario}")
        
    assert response_get_metas.status_code == 200
    
    lista_metas = response_get_metas.json()
    # Soporta tanto PascalCase como snake_case para evitar fallos de mapeo en DB
    meta_creada = next(
        (m for m in lista_metas if m.get("NombreMeta") == nombre_meta_e2e or m.get("nombre_meta") == nombre_meta_e2e), 
        None
    )
    
    assert meta_creada is not None, "La meta no aparece en la lista del usuario"
    id_meta_generado = meta_creada.get("IdMeta") or meta_creada.get("id_meta") or meta_creada.get("id")

    # ==========================================
    # PASO 6: LIMPIEZA (TEARDOWN)
    # ==========================================
    if id_meta_generado:
        response_delete_meta = client.delete(f"/api/metas/{id_meta_generado}")
        if response_delete_meta.status_code == 404:
            response_delete_meta = client.delete(f"/metas/{id_meta_generado}")
            
        assert response_delete_meta.status_code == 200, "Fallo al eliminar la meta de prueba"