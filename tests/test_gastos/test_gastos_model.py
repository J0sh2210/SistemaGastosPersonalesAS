import pytest
from pydantic import ValidationError
from models.schemas import GastoCreate


def test_gasto_create_valido():
    gasto = GastoCreate(
        Concepto="Comida",
        Monto=50.75,
        IdCliente=1,
        IdCategoria=2
    )

    assert gasto.Concepto == "Comida"
    assert gasto.Monto == 50.75
    assert gasto.IdCliente == 1
    assert gasto.IdCategoria == 2


def test_gasto_create_sin_categoria():
    gasto = GastoCreate(
        Concepto="Transporte",
        Monto=25.00,
        IdCliente=1
    )

    assert gasto.Concepto == "Transporte"
    assert gasto.IdCategoria is None


def test_gasto_monto_negativo_no_permitido():
    with pytest.raises(ValidationError):
        GastoCreate(
            Concepto="Comida",
            Monto=-10,
            IdCliente=1,
            IdCategoria=2
        )


def test_gasto_concepto_vacio_no_permitido():
    with pytest.raises(ValidationError):
        GastoCreate(
            Concepto="",
            Monto=50,
            IdCliente=1,
            IdCategoria=2
        )
