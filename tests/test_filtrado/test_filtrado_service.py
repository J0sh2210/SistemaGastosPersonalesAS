import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from services.filtrado_service import filtrar_movimientos_por_mes

def test_filtrar_movimientos_por_mes_exitoso():
    """Prueba que el servicio retorne los datos correctamente cuando los parámetros son válidos."""
    mock_db = MagicMock(spec=Session)
    
    mock_row_1 = MagicMock()
    mock_row_1._mapping = {"id": 1, "monto": 150.0, "categoria": "Comida", "fecha": "2026-05-10"}
    mock_row_2 = MagicMock()
    mock_row_2._mapping = {"id": 2, "monto": 45.5, "categoria": "Transporte", "fecha": "2026-05-12"}
    
    # Configuramos el mock para que devuelva nuestra lista simulada al usar fetchall()
    mock_db.execute.return_value.fetchall.return_value = [mock_row_1, mock_row_2]

    # Ejecutamos tu función con datos válidos
    resultado = filtrar_movimientos_por_mes(mes=5, anio=2026, db=mock_db)

    # Validaciones (Asserts)
    assert len(resultado) == 2
    assert resultado[0]["categoria"] == "Comida"
    assert resultado[1]["monto"] == 45.5
    # Verificamos que se haya llamado a la base de datos exactamente una vez
    mock_db.execute.assert_called_once()


# --- 2. CASOS NEGATIVOS / VALIDACIONES ---

def test_filtrar_movimientos_mes_invalido_menor():
    """Prueba que lance error 400 si el mes es menor a 1."""
    mock_db = MagicMock(spec=Session)
    
    # Verificamos que levante la excepción HTTPException esperada
    with pytest.raises(HTTPException) as exc_info:
        filtrar_movimientos_por_mes(mes=0, anio=2026, db=mock_db)
        
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El mes debe estar entre 1 y 12"

def test_filtrar_movimientos_mes_invalido_mayor():
    """Prueba que lance error 400 si el mes es mayor a 12."""
    mock_db = MagicMock(spec=Session)
    
    with pytest.raises(HTTPException) as exc_info:
        filtrar_movimientos_por_mes(mes=13, anio=2026, db=mock_db)
        
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El mes debe estar entre 1 y 12"

def test_filtrar_movimientos_anio_invalido():
    """Prueba que lance error 400 si el año es menor a 2000."""
    mock_db = MagicMock(spec=Session)
    
    with pytest.raises(HTTPException) as exc_info:
        filtrar_movimientos_por_mes(mes=6, anio=1999, db=mock_db)
        
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "El anio no es valido"