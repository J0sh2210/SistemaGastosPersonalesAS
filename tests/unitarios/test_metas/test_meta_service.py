from datetime import date, timedelta
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

# Importamos las funciones de tu servicio
from services.meta_service import crear_meta, actualizar_cantidad_ahorro, eliminar_meta

# Clase Mock auxiliar para simular el objeto 'data' (Pydantic Schema)
class MockMetaData:
    def __init__(self, id_usuario=1, nombre_meta="Ahorro Carro", monto_objetivo=5000.0, fecha_limite=None, monto_actual=0.0):
        self.id_usuario = id_usuario
        self.nombre_meta = nombre_meta
        self.monto_objetivo = monto_objetivo
        self.fecha_limite = fecha_limite if fecha_limite else date.today() + timedelta(days=30)
        self.monto_actual = monto_actual


# --- PRUEBAS PARA CREAR META ---

@patch("services.meta_service.engine")
def test_crear_meta_servicio_exitoso(mock_engine):
    """Prueba que una meta válida se cree correctamente y devuelva su ID."""
    # Configuración del mock de base de datos para simular .fetchone()[0] -> id_meta
    mock_conn = MagicMock()
    mock_resultado = MagicMock()
    mock_resultado.fetchone.return_value = [100]  # Simula el ID generado por la BD
    mock_conn.execute.return_value = mock_resultado
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    data_valida = MockMetaData()
    
    resultado = crear_meta(data_valida)
    
    assert resultado["mensaje"] == "Meta creada correctamente"
    assert resultado["id_meta"] == 100


def test_crear_meta_nombre_vacio():
    """Prueba que falle si el nombre de la meta está vacío."""
    data_invalida = MockMetaData(nombre_meta="   ")
    
    with pytest.raises(HTTPException) as exc_info:
        crear_meta(data_invalida)
        
    assert exc_info.value.status_code == 400
    assert "El nombre de la meta no puede estar vacío" in exc_info.value.detail


def test_crear_meta_monto_objetivo_invalido():
    """Prueba que falle si el monto objetivo es menor o igual a cero."""
    data_invalida = MockMetaData(monto_objetivo=0)
    
    with pytest.raises(HTTPException) as exc_info:
        crear_meta(data_invalida)
        
    assert exc_info.value.status_code == 400
    assert "El monto objetivo debe ser mayor a cero" in exc_info.value.detail


def test_crear_meta_fecha_anterior_a_hoy():
    """Prueba que falle si la fecha límite ya pasó."""
    fecha_pasada = date.today() - timedelta(days=1)
    data_invalida = MockMetaData(fecha_limite=fecha_pasada)
    
    with pytest.raises(HTTPException) as exc_info:
        crear_meta(data_invalida)
        
    assert exc_info.value.status_code == 400
    assert "La fecha límite no puede ser anterior a hoy" in exc_info.value.detail


def test_crear_meta_monto_actual_negativo():
    """Prueba que falle si el monto inicial guardado es negativo."""
    data_invalida = MockMetaData(monto_actual=-50.0)
    
    with pytest.raises(HTTPException) as exc_info:
        crear_meta(data_invalida)
        
    assert exc_info.value.status_code == 400
    assert "El monto actual no puede ser negativo" in exc_info.value.detail


# --- PRUEBAS PARA ACTUALIZAR CANTIDAD ---

@patch("services.meta_service.engine")
def test_actualizar_cantidad_servicio_exitoso(mock_engine):
    """Prueba que la cantidad se actualice con éxito si la meta existe."""
    mock_conn = MagicMock()
    mock_resultado = MagicMock()
    mock_resultado.rowcount = 1  # Simula que encontró y modificó 1 registro
    mock_conn.execute.return_value = mock_resultado
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    data_update = MockMetaData(monto_actual=150.0)
    
    resultado = actualizar_cantidad_ahorro(id_meta=1, data=data_update)
    assert resultado["mensaje"] == "Cantidad de ahorro actualizada correctamente"


@patch("services.meta_service.engine")
def test_actualizar_cantidad_meta_no_encontrada(mock_engine):
    """Prueba que lance un 404 si el ID de la meta no existe al actualizar."""
    mock_conn = MagicMock()
    mock_resultado = MagicMock()
    mock_resultado.rowcount = 0  # Simula que no afectó ninguna fila
    mock_conn.execute.return_value = mock_resultado
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    data_update = MockMetaData(monto_actual=150.0)
    
    with pytest.raises(HTTPException) as exc_info:
        actualizar_cantidad_ahorro(id_meta=999, data=data_update)
        
    assert exc_info.value.status_code == 404
    assert "Meta no encontrada" in exc_info.value.detail


def test_actualizar_cantidad_negativa():
    """Prueba que valide y aborte si el nuevo monto es negativo."""
    data_invalida = MockMetaData(monto_actual=-10.0)
    
    with pytest.raises(HTTPException) as exc_info:
        actualizar_cantidad_ahorro(id_meta=1, data=data_invalida)
        
    assert exc_info.value.status_code == 400
    assert "La cantidad ahorrada no puede ser negativa" in exc_info.value.detail


# --- PRUEBAS PARA ELIMINAR META ---

@patch("services.meta_service.engine")
def test_eliminar_meta_servicio_exitoso(mock_engine):
    """Prueba que elimine la meta correctamente si el ID existe."""
    mock_conn = MagicMock()
    mock_resultado = MagicMock()
    mock_resultado.rowcount = 1  # Fila eliminada con éxito
    mock_conn.execute.return_value = mock_resultado
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    resultado = eliminar_meta(id_meta=5)
    assert resultado["mensaje"] == "Meta de ahorro eliminada correctamente"


@patch("services.meta_service.engine")
def test_eliminar_meta_no_encontrada(mock_engine):
    """Prueba que lance un 404 si la meta a eliminar no existe."""
    mock_conn = MagicMock()
    mock_resultado = MagicMock()
    mock_resultado.rowcount = 0  # No se borró nada
    mock_conn.execute.return_value = mock_resultado
    mock_engine.begin.return_value.__enter__.return_value = mock_conn

    with pytest.raises(HTTPException) as exc_info:
        eliminar_meta(id_meta=999)
        
    assert exc_info.value.status_code == 404
    assert "Meta de ahorro no encontrada" in exc_info.value.detail