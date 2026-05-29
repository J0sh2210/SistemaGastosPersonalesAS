from unittest.mock import patch, MagicMock
from services.budget_service import registrar_presupuesto


def test_registrar_presupuesto_exitoso():
    with patch("services.budget_service.sp_registrar_presupuesto") as mock_sp:
        mock_sp.return_value = None
        with patch.dict("sys.modules", {"sabeerquees.db_manager": MagicMock(sp_registrar_presupuesto=mock_sp)}):
            result = registrar_presupuesto(1, "2026-05", "Comida", 500.0)
            assert result["success"] == True
            assert "500" in result["message"]


def test_registrar_presupuesto_categoria_none():
    with patch("services.budget_service.sp_registrar_presupuesto") as mock_sp:
        mock_sp.return_value = None
        with patch.dict("sys.modules", {"sabeerquees.db_manager": MagicMock(sp_registrar_presupuesto=mock_sp)}):
            result = registrar_presupuesto(1, "2026-05", None, 300.0)
            assert result["success"] == True
            assert "General" in result["message"]


def test_registrar_presupuesto_monto_en_mensaje():
    with patch("services.budget_service.sp_registrar_presupuesto") as mock_sp:
        mock_sp.return_value = None
        with patch.dict("sys.modules", {"sabeerquees.db_manager": MagicMock(sp_registrar_presupuesto=mock_sp)}):
            result = registrar_presupuesto(1, "2026-05", "Transporte", 150.0)
            assert "150" in result["message"]
