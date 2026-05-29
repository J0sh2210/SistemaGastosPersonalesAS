from pydantic import ValidationError
from models.usuario_model import RegistroUsuario, LoginUsuario, ActualizarUsuario, UsuarioResponse

def test_registro_usuario_schema_valido():
    usuario = RegistroUsuario(
        username="angelica@test.com",
        password="123456",
        primerNombre="Angelica",
        primerApellido="Mejia"
    )

    assert usuario.username == "angelica@test.com"
    assert usuario.segundoNombre is None

def test_login_usuario_schema_valido():
    login = LoginUsuario(
        username="angelica@test.com",
        password="123456"
    )

    assert login.username == "angelica@test.com"
    assert login.password == "123456"

def test_actualizar_usuario_schema_valido():
    usuario = ActualizarUsuario(
        primerNombre="Angelica",
        primerApellido="Mejia"
    )

    assert usuario.primerNombre == "Angelica"
    assert usuario.segundoApellido is None

def test_usuario_response_schema_valido():
    usuario = UsuarioResponse(
        IdCliente=1,
        usuario="angelica@test.com",
        nombre="Angelica",
        apellido="Mejia"
    )

    assert usuario.IdCliente == 1
    assert usuario.usuario == "angelica@test.com"