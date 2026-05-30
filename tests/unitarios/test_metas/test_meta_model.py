from datetime import date
import pytest
from pydantic import ValidationError

# Importamos tus modelos Pydantic desde schemas
from models.meta_model import MetaAhorroCreate, ActualizarCantidadMeta

# --- PRUEBAS PARA METAAHORROCREATE ---

def test_meta_ahorro_create_valido():
    """Prueba que el modelo acepte un diccionario con todos los datos correctos."""
    datos_validos = {
        "id_usuario": 1,
        "nombre_meta": "Fondo de Emergencia",
        "monto_objetivo": 2500.50,
        "fecha_limite": "2026-12-31",  # Pydantic convierte el string a objeto date automáticamente
        "monto_actual": 100.0
    }
    
    modelo = MetaAhorroCreate(**datos_validos)
    
    assert modelo.id_usuario == 1
    assert modelo.nombre_meta == "Fondo de Emergencia"
    assert modelo.monto_objetivo == 2500.50
    assert modelo.fecha_limite == date(2026, 12, 31)
    assert modelo.monto_actual == 100.0


def test_meta_ahorro_create_faltan_campos():
    """Prueba que el modelo falle si no se le envían los campos obligatorios."""
    datos_incompletos = {
        "id_usuario": 1,
        "nombre_meta": "Bici Nueva"
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MetaAhorroCreate(**datos_incompletos)
        
    errores = exc_info.value.errors()
    campos_faltantes = [err["loc"][0] for err in errores]
    
    assert "monto_objetivo" in campos_faltantes
    assert "fecha_limite" in campos_faltantes
    assert "monto_actual" in campos_faltantes


def test_meta_ahorro_create_tipos_invalidos():
    """Prueba que el modelo rechace tipos de datos incorrectos."""
    datos_erroneos = {
        "id_usuario": "no_soy_un_entero", 
        "nombre_meta": "Viaje",
        "monto_objetivo": "mucho_dinero", 
        "fecha_limite": "fecha-invalida-2026", 
        "monto_actual": 0.0
    }
    
    with pytest.raises(ValidationError) as exc_info:
        MetaAhorroCreate(**datos_erroneos)
        
    errores = exc_info.value.errors()
    campos_con_error = [err["loc"][0] for err in errores]
    
    assert "id_usuario" in campos_con_error
    assert "monto_objetivo" in campos_con_error
    assert "fecha_limite" in campos_con_error


# --- PRUEBAS PARA ACTUALIZARCANTIDADMETA ---

def test_actualizar_cantidad_meta_valido():
    """Prueba que el modelo de actualización acepte un float válido."""
    modelo = ActualizarCantidadMeta(monto_actual=850.75)
    assert modelo.monto_actual == 850.75


def test_actualizar_cantidad_meta_tipo_invalido():
    """Prueba que el modelo de actualización rechace un tipo de dato no numérico."""
    with pytest.raises(ValidationError):
        ActualizarCantidadMeta(monto_actual="quinientos_pesos")