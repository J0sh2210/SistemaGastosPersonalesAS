def test_crear_categoria_servicio():
    data = CategoriaCreate(nombre_categoria="Comida", id_tipo_movimiento=1, id_tipo_categoria=2)
    with patch("services.categoria_service.engine") as mock_engine:
        mock_conn = MagicMock()
        mock_engine.begin.return_value.__enter__ = MagicMock(return_value=mock_conn)
        mock_engine.begin.return_value.__exit__ = MagicMock(return_value=False)
        result = crear_categoria(data)
        assert "mensaje" in result