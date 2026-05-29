from models.categoria_model import CategoriaCreate, CategoriaUpdate

def test_categoria_create_valida():
    cat = CategoriaCreate(nombre_categoria="Comida", id_tipo_movimiento=1, id_tipo_categoria=2)
    assert cat.nombre_categoria == "Comida"
    assert cat.id_tipo_movimiento == 1
    assert cat.id_tipo_categoria == 2

def test_categoria_update_parcial():
    cat = CategoriaUpdate(nombre_categoria="Transporte")
    assert cat.nombre_categoria == "Transporte"
    assert cat.id_tipo_movimiento is None
    assert cat.id_tipo_categoria is None

def test_categoria_update_vacia():
    cat = CategoriaUpdate()
    assert cat.nombre_categoria is None
    assert cat.id_tipo_movimiento is None
    assert cat.id_tipo_categoria is None