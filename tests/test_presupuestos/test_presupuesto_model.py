import pytest
from pydantic import ValidationError
from models.presupuesto_model import PresupuestoCreate, PresupuestoUpdate, PresupuestoResponse


def test_presupuesto_create_valido():
    p = PresupuestoCreate(
        monto_presupuesto=500.0,
        id_categoria=1,
        mes_aplicacion="2026-05",
        id_usuario=1
    )
    assert p.monto_presupuesto == 500.0
    assert p.mes_aplicacion == "2026-05"


def test_presupuesto_create_sin_categoria():
    p = PresupuestoCreate(
        monto_presupuesto=300.0,
        mes_aplicacion="2026-05",
        id_usuario=1
    )
    assert p.id_categoria is None


def test_presupuesto_create_sin_usuario_falla():
    with pytest.raises(ValidationError):
        PresupuestoCreate(
            monto_presupuesto=500.0,
            mes_aplicacion="2026-05"
        )


def test_presupuesto_update_todos_opcionales():
    p = PresupuestoUpdate()
    assert p.monto_presupuesto is None
    assert p.id_categoria is None
    assert p.mes_aplicacion is None
    assert p.id_usuario is None


def test_presupuesto_update_parcial():
    p = PresupuestoUpdate(monto_presupuesto=999.0)
    assert p.monto_presupuesto == 999.0
    assert p.id_categoria is None


def test_presupuesto_response_valido():
    p = PresupuestoResponse(
        id_presupuesto=1,
        monto_presupuesto=500.0,
        categoria="Comida",
        mes_aplicacion="2026-05",
        id_usuario=1
    )
    assert p.id_presupuesto == 1
    assert p.categoria == "Comida"
