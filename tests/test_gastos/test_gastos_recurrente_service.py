from services.gasto_recurrente_service import desactivar_gasto_recurrente


class FakeGasto:
    def __init__(self):
        self.IdGastoRecurrente = 1
        self.Activo = True


class FakeQuery:
    def __init__(self, gasto):
        self.gasto = gasto

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.gasto


class FakeDB:
    def __init__(self, gasto):
        self.gasto = gasto

    def query(self, model):
        return FakeQuery(self.gasto)

    def commit(self):
        pass


def test_desactivar_gasto_recurrente_correctamente():

    gasto = FakeGasto()
    db = FakeDB(gasto)

    response = desactivar_gasto_recurrente(db, 1)

    assert response["success"] is True
    assert gasto.Activo is False


def test_desactivar_gasto_no_encontrado():

    db = FakeDB(None)

    response = desactivar_gasto_recurrente(db, 999)

    assert response["success"] is False