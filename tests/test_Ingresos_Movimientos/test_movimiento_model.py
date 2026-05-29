from models.movimiento_model import EditarCategoriaRequest, DiferenciaResponse
from pydantic import ValidationError
import pytest

def test_editar_categoria_request_valido():
    # Act
    request = EditarCategoriaRequest(idCategoria=5)
    
    # Assert
    assert request.idCategoria == 5

def test_editar_categoria_request_invalido():
    # Act & Assert
    with pytest.raises(ValidationError):
        EditarCategoriaRequest(idCategoria="no_es_entero")

def test_diferencia_response():
    # Act
    response = DiferenciaResponse(total=1500.50)
    
    # Assert
    assert response.total == 1500.50
    assert isinstance(response.total, float)