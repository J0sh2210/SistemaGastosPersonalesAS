import pytest
from fastapi import HTTPException
from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

def test_hash_password_no_es_texto_plano():
    password = "123456"
    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)

def test_verify_password_correcta():
    password = "123456"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True

def test_verify_password_incorrecta():
    password = "123456"
    hashed = hash_password(password)

    assert verify_password("incorrecta", hashed) is False

def test_create_access_token_devuelve_string():
    token = create_access_token({"sub": "angelica@test.com"})

    assert isinstance(token, str)
    assert len(token) > 20

def test_get_current_user_token_valido():
    token = create_access_token({"sub": "angelica@test.com"})
    usuario = get_current_user(token)

    assert usuario == "angelica@test.com"

def test_get_current_user_token_invalido():
    with pytest.raises(HTTPException) as error:
        get_current_user("token_invalido")

    assert error.value.status_code == 401