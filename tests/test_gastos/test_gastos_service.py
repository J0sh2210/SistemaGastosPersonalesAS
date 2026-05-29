import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from services.gasto_service import (
    obtener_gastos,
    crear_nuevo_gasto,
    eliminar_gasto_db,
    actualizar_gasto_db,
    ID_TIPO_GASTO
)
from models.schemas import GastoCreate


def test_obtener_gastos():
    db = MagicMock()

    obtener_gastos(db)

    db.query.return_value.filter.return_value.all.assert_called_once()


def test_crear_nuevo_gasto():
    db = MagicMock()
    gasto_data = GastoCreate(
        Concepto="Comida",
        Monto=50,
        IdCliente=1,
        IdCategoria=2
    )

    resultado = crear_nuevo_gasto(db, gasto_data)

    assert resultado.Concepto == "Comida"
    assert resultado.Monto == 50
    assert resultado.IdCliente == 1
    assert resultado.IdCategoria == 2
    assert resultado.IdTipo == ID_TIPO_GASTO

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_eliminar_gasto_no_encontrado():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as error:
        eliminar_gasto_db(db, 999)

    assert error.value.status_code == 404
    assert error.value.detail == "Gasto no encontrado"


def test_actualizar_gasto_no_encontrado():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    gasto_data = GastoCreate(
        Concepto="Comida",
        Monto=50,
        IdCliente=1,
        IdCategoria=2
    )

    with pytest.raises(HTTPException) as error:
        actualizar_gasto_db(db, 999, gasto_data)

    assert error.value.status_code == 404
    assert error.value.detail == "Gasto no encontrado"