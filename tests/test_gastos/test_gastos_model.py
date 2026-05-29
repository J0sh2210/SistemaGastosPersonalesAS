from models.gasto_recurrente_model import GastoRecurrente
from datetime import date


def test_modelo_gasto_recurrente():

    gasto = GastoRecurrente(
        Concepto="Netflix",
        Monto=250,
        FechaInicio=date.today(),
        Frecuencia="mensual",
        IdCliente=1,
        Activo=True
    )

    assert gasto.Concepto == "Netflix"
    assert gasto.Monto == 250
    assert gasto.Frecuencia == "mensual"
    assert gasto.IdCliente == 1
    assert gasto.Activo is True