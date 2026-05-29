import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from models.schemas import IngresoCreate, IngresoUpdate
from services.ingreso_service import IngresoService

def test_registrar_ingreso():
    # Arrange
    mock_db = MagicMock()
    mock_ingreso = IngresoCreate(Concepto="Venta", Monto=100.0, IdCliente=1, IdMovimiento=10)
    mock_result = MagicMock()
    mock_result._mapping = {"IdMovimiento": 10, "Estado": "Registrado"}
    mock_db.execute.return_value.fetchone.return_value = mock_result

    # Act
    resultado = IngresoService.registrar(mock_db, mock_ingreso)

    # Assert
    assert resultado == {"IdMovimiento": 10, "Estado": "Registrado"}
    mock_db.execute.assert_called_once()
    mock_db.commit.assert_called_once()

def test_editar_ingreso_exitoso():
    # Arrange
    mock_db = MagicMock()
    mock_ingreso_update = IngresoUpdate(Concepto="Venta Editada", Monto=150.0)
    mock_result = MagicMock()
    mock_result._mapping = {"IdMovimiento": 1, "Concepto": "Venta Editada"}
    mock_db.execute.return_value.fetchone.return_value = mock_result

    # Act
    resultado = IngresoService.editar(mock_db, 1, mock_ingreso_update)

    # Assert
    assert resultado == {"IdMovimiento": 1, "Concepto": "Venta Editada"}
    mock_db.commit.assert_called_once()

def test_editar_ingreso_no_encontrado():
    # Arrange
    mock_db = MagicMock()
    mock_ingreso_update = IngresoUpdate(Concepto="Venta Editada", Monto=150.0)
    mock_db.execute.return_value.fetchone.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        IngresoService.editar(mock_db, 99, mock_ingreso_update)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ingreso no encontrado o pertenece a un Egreso"