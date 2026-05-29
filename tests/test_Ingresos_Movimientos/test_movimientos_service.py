import pytest
from unittest.mock import MagicMock, patch
from services.movimientos_service import (
    MovimientoService, 
    editar_categoria_movimiento, 
    calcular_diferencia, 
    filtrar_movimientos
)

def test_obtener_movimientos_mes_actual():
    # Arrange
    mock_db = MagicMock()
    mock_row = MagicMock()
    mock_row._mapping = {"IdMovimiento": 1, "Concepto": "Prueba"}
    mock_db.execute.return_value.fetchall.return_value = [mock_row]

    # Act
    resultado = MovimientoService.obtener_movimientos_mes_actual(mock_db, 1)

    # Assert
    assert len(resultado) == 1
    assert resultado[0] == {"IdMovimiento": 1, "Concepto": "Prueba"}

@patch("services.movimientos_service.SessionLocal")
def test_editar_categoria_movimiento_no_existe(mock_session_local):
    # Arrange
    mock_db = mock_session_local.return_value
    mock_db.execute.return_value.fetchone.return_value = None # Simula que no encuentra el movimiento

    # Act
    resultado = editar_categoria_movimiento(99, 1)

    # Assert
    assert resultado == "MOVIMIENTO_NO_EXISTE"
    mock_db.close.assert_called_once()

@patch("services.movimientos_service.SessionLocal")
def test_editar_categoria_exito(mock_session_local):
    # Arrange
    mock_db = mock_session_local.return_value
    # Simula que encuentra tanto el movimiento como la categoría (llamadas secuenciales a fetchone)
    mock_db.execute.return_value.fetchone.side_effect = [{"1": 1}, {"1": 1}]

    # Act
    resultado = editar_categoria_movimiento(1, 2)

    # Assert
    assert resultado == "OK"
    mock_db.commit.assert_called_once()
    mock_db.close.assert_called_once()