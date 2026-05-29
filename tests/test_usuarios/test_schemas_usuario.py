import pytest
from pydantic import ValidationError
from models.usuario_model import RegistroUsuario, LoginUsuario


def test_registro_usuario_campos_requeridos():
    with pytest.raises(ValidationError):
        RegistroUsuario()


def test_login_usuario_campos_requeridos():
    with pytest.raises(ValidationError):
        LoginUsuario()


def test_registro_usuario_username_vacio():
    usuario = RegistroUsuario(
        username="",
        password="123456",
        primerNombre="Angelica",
        primerApellido="Mejia"
    )

    assert usuario.username == ""


def test_login_usuario_password_vacia():
    login = LoginUsuario(
        username="angelica@test.com",
        password=""
    )

    assert login.password == ""