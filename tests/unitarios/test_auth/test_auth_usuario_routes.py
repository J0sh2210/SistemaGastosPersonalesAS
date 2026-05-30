from fastapi.testclient import TestClient
from main import app
from routes.usuario_routes import get_db
from services.auth_service import create_access_token, hash_password

client = TestClient(app)


class FakeQuery:
    def __init__(self, result):
        self.result = result

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.result


class FakeDB:
    def __init__(self):
        self.cliente = None
        self.usuario = None
        self.commits = 0

    def add(self, obj):
        if obj.__class__.__name__ == "Cliente":
            obj.IdCliente = 1
            self.cliente = obj
        else:
            self.usuario = obj

    def commit(self):
        self.commits += 1

    def refresh(self, obj):
        obj.IdCliente = 1

    def rollback(self):
        pass

    def close(self):
        pass

    def query(self, model):
        if model.__name__ == "Usuario":
            return FakeQuery(self.usuario)
        if model.__name__ == "Cliente":
            return FakeQuery(self.cliente)
        return FakeQuery(None)


def override_get_db():
    db = FakeDB()
    yield db


def test_registro_usuario_correcto_mock():
    app.dependency_overrides[get_db] = override_get_db

    response = client.post("/usuarios/registro", json={
        "username": "angelica@test.com",
        "password": "123456",
        "primerNombre": "Angelica",
        "segundoNombre": None,
        "primerApellido": "Mejia",
        "segundoApellido": None
    })

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["message"] == "Usuario registrado correctamente"
    assert response.json()["usuario"] == "angelica@test.com"


def test_login_correcto_mock():
    fake_db = FakeDB()

    class UsuarioFake:
        NombreUsuario = "angelica@test.com"
        Contrasena = hash_password("123456")
        IdCliente = 1

    fake_db.usuario = UsuarioFake()

    def override_get_db_login():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db_login

    response = client.post("/usuarios/login", data={
        "username": "angelica@test.com",
        "password": "123456"
    })

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_obtener_perfil_con_token_mock():
    fake_db = FakeDB()

    class UsuarioFake:
        NombreUsuario = "angelica@test.com"
        Contrasena = hash_password("123456")
        IdCliente = 1

    class ClienteFake:
        IdCliente = 1
        PrimerNombre = "Angelica"
        SegundoNombre = None
        PrimerApellido = "Mejia"
        SegundoApellido = None
        Estado = "A"

    fake_db.usuario = UsuarioFake()
    fake_db.cliente = ClienteFake()

    def override_get_db_perfil():
        yield fake_db

    token = create_access_token({"sub": "angelica@test.com"})

    app.dependency_overrides[get_db] = override_get_db_perfil

    response = client.get("/usuarios/perfil", headers={
        "Authorization": f"Bearer {token}"
    })

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["usuario"] == "angelica@test.com"
    assert response.json()["nombre"] == "Angelica"


def test_actualizar_perfil_mock():
    fake_db = FakeDB()

    class UsuarioFake:
        NombreUsuario = "angelica@test.com"
        IdCliente = 1

    class ClienteFake:
        IdCliente = 1
        PrimerNombre = "Angelica"
        SegundoNombre = None
        PrimerApellido = "Mejia"
        SegundoApellido = None
        Estado = "A"

    fake_db.usuario = UsuarioFake()
    fake_db.cliente = ClienteFake()

    def override_get_db_update():
        yield fake_db

    token = create_access_token({"sub": "angelica@test.com"})

    app.dependency_overrides[get_db] = override_get_db_update

    response = client.put("/usuarios/perfil", json={
        "primerNombre": "Angie",
        "segundoNombre": None,
        "primerApellido": "Mejia",
        "segundoApellido": None
    }, headers={
        "Authorization": f"Bearer {token}"
    })

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["message"] == "Perfil actualizado correctamente"


def test_eliminar_cuenta_mock():
    fake_db = FakeDB()

    class UsuarioFake:
        NombreUsuario = "angelica@test.com"
        IdCliente = 1

    class ClienteFake:
        IdCliente = 1
        Estado = "A"

    fake_db.usuario = UsuarioFake()
    fake_db.cliente = ClienteFake()

    def override_get_db_delete():
        yield fake_db

    token = create_access_token({"sub": "angelica@test.com"})

    app.dependency_overrides[get_db] = override_get_db_delete

    response = client.delete("/usuarios/cuenta", headers={
        "Authorization": f"Bearer {token}"
    })

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["message"] == "El usuario fue eliminado exitosamente"