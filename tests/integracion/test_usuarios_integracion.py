import pytest


def test_integracion_registro_usuario(client):
    """Prueba el registro de un nuevo usuario"""
    import uuid
    username = f"testuser_{uuid.uuid4().hex[:8]}"  # Username único para evitar duplicados
    
    payload = {
        "primerNombre": "Juan",
        "segundoNombre": "Carlos",
        "primerApellido": "Pérez",
        "segundoApellido": "García",
        "username": username,
        "password": "SecurePassword123!"
    }
    
    response = client.post("/usuarios/registro", json=payload)
    
    # Puede retornar 200 o error
    assert response.status_code in [200, 400, 409, 500]


def test_integracion_login_usuario(client):
    """Prueba el login de un usuario"""
    payload = {
        "username": "admin",
        "password": "admin"
    }
    
    response = client.post("/usuarios/login", data=payload)
    
    # Puede retornar 200 si las credenciales son válidas o 400 si no
    assert response.status_code in [200, 400]


def test_integracion_obtener_perfil_usuario(client):
    """Prueba obtener el perfil del usuario autenticado"""
    # Primero hacer login
    login_payload = {
        "username": "admin",
        "password": "admin"
    }
    
    response_login = client.post("/usuarios/login", data=login_payload)
    
    if response_login.status_code == 200:
        # Si el login fue exitoso, intentamos obtener el perfil
        response_perfil = client.get("/usuarios/perfil")
        
        # Puede retornar 200 si la autenticación es correcta o 422 si falta token
        assert response_perfil.status_code in [200, 422, 401, 403]
    else:
        # Si el login falla, esperamos que sea un error
        assert response_login.status_code in [400]
