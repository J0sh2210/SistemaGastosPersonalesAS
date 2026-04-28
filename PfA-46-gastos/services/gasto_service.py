from database import engine
from sqlalchemy import text
from fastapi import HTTPException
from models.gasto_model import GastoCreate, GastoUpdate


# ID de tipo de movimiento para Egreso / Gasto
ID_TIPO_EGRESO = 2


def existe_cliente(id_cliente: int) -> bool:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM Cliente WHERE IdCliente = :id"),
            {"id": id_cliente}
        ).fetchone()
        return result is not None


def existe_categoria(id_categoria: int) -> bool:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM CategoriaMovimiento WHERE IdCategoria = :id"),
            {"id": id_categoria}
        ).fetchone()
        return result is not None


def existe_gasto(id_gasto: int) -> bool:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM Movimiento WHERE IdMovimiento = :id"),
            {"id": id_gasto}
        ).fetchone()
        return result is not None


def crear_gasto(data: GastoCreate):
    if not data.concepto or not data.concepto.strip():
        raise HTTPException(status_code=400, detail="El concepto es requerido")

    if len(data.concepto.strip()) > 30:
        raise HTTPException(status_code=400, detail="El concepto no puede exceder 30 caracteres")

    if data.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")

    if not existe_cliente(data.id_cliente):
        raise HTTPException(status_code=400, detail="El cliente no existe")

    if not existe_categoria(data.id_categoria):
        raise HTTPException(status_code=400, detail="La categoría no existe")

    # Si no hay fecha, usamos GETDATE() en SQL Server en vez de pasar NULL
    if data.fecha_movimiento is None:
        query = text("""
            INSERT INTO Movimiento (Concepto, Monto, FechaMovimiento, IdCliente, IdTipo, IdCategoria)
            VALUES (:concepto, :monto, GETDATE(), :id_cliente, :id_tipo, :id_categoria)
        """)
        params = {
            "concepto": data.concepto.strip(),
            "monto": data.monto,
            "id_cliente": data.id_cliente,
            "id_tipo": ID_TIPO_EGRESO,
            "id_categoria": data.id_categoria
        }
    else:
        query = text("""
            INSERT INTO Movimiento (Concepto, Monto, FechaMovimiento, IdCliente, IdTipo, IdCategoria)
            VALUES (:concepto, :monto, :fecha, :id_cliente, :id_tipo, :id_categoria)
        """)
        params = {
            "concepto": data.concepto.strip(),
            "monto": data.monto,
            "fecha": data.fecha_movimiento,
            "id_cliente": data.id_cliente,
            "id_tipo": ID_TIPO_EGRESO,
            "id_categoria": data.id_categoria
        }

    with engine.begin() as conn:
        conn.execute(query, params)

    return {"mensaje": "Gasto registrado correctamente"}


def editar_gasto(id_gasto: int, data: GastoUpdate):
    if not existe_gasto(id_gasto):
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    campos = []
    valores = {"id": id_gasto}

    if data.concepto is not None:
        concepto = data.concepto.strip()
        if not concepto:
            raise HTTPException(status_code=400, detail="El concepto no puede estar vacío")
        if len(concepto) > 30:
            raise HTTPException(status_code=400, detail="El concepto no puede exceder 30 caracteres")
        campos.append("Concepto = :concepto")
        valores["concepto"] = concepto

    if data.monto is not None:
        if data.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")
        campos.append("Monto = :monto")
        valores["monto"] = data.monto

    if data.id_categoria is not None:
        if not existe_categoria(data.id_categoria):
            raise HTTPException(status_code=400, detail="La categoría no existe")
        campos.append("IdCategoria = :id_categoria")
        valores["id_categoria"] = data.id_categoria

    if data.fecha_movimiento is not None:
        campos.append("FechaMovimiento = :fecha")
        valores["fecha"] = data.fecha_movimiento

    if not campos:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    query = text(f"""
        UPDATE Movimiento
        SET {', '.join(campos)}
        WHERE IdMovimiento = :id
    """)

    with engine.begin() as conn:
        resultado = conn.execute(query, valores)

        if resultado.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return {"mensaje": "Gasto actualizado correctamente"}


def obtener_gastos():
    query = text("""
        SELECT
            m.IdMovimiento,
            m.Concepto,
            m.Monto,
            m.FechaMovimiento,
            m.IdCliente,
            CONCAT(c.PrimerNombre, ' ', c.PrimerApellido) AS NombreCliente,
            m.IdCategoria,
            cm.NombreCategoria
        FROM Movimiento m
        INNER JOIN Cliente c ON m.IdCliente = c.IdCliente
        INNER JOIN CategoriaMovimiento cm ON m.IdCategoria = cm.IdCategoria
        WHERE m.IdTipo = :id_tipo
        ORDER BY m.FechaMovimiento DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"id_tipo": ID_TIPO_EGRESO})

        return [
            {
                "id": row[0],
                "concepto": row[1],
                "monto": float(row[2]),
                "fecha_movimiento": row[3].isoformat() if row[3] else None,
                "id_cliente": row[4],
                "nombre_cliente": row[5],
                "id_categoria": row[6],
                "nombre_categoria": row[7]
            }
            for row in result
        ]


def obtener_gasto(id_gasto: int):
    query = text("""
        SELECT
            m.IdMovimiento,
            m.Concepto,
            m.Monto,
            m.FechaMovimiento,
            m.IdCliente,
            CONCAT(c.PrimerNombre, ' ', c.PrimerApellido) AS NombreCliente,
            m.IdCategoria,
            cm.NombreCategoria
        FROM Movimiento m
        INNER JOIN Cliente c ON m.IdCliente = c.IdCliente
        INNER JOIN CategoriaMovimiento cm ON m.IdCategoria = cm.IdCategoria
        WHERE m.IdMovimiento = :id AND m.IdTipo = :id_tipo
    """)

    with engine.connect() as conn:
        row = conn.execute(query, {"id": id_gasto, "id_tipo": ID_TIPO_EGRESO}).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")

        return {
            "id": row[0],
            "concepto": row[1],
            "monto": float(row[2]),
            "fecha_movimiento": row[3].isoformat() if row[3] else None,
            "id_cliente": row[4],
            "nombre_cliente": row[5],
            "id_categoria": row[6],
            "nombre_categoria": row[7]
        }


def eliminar_gasto(id_gasto: int):
    if not existe_gasto(id_gasto):
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    query = text("DELETE FROM Movimiento WHERE IdMovimiento = :id")

    with engine.begin() as conn:
        resultado = conn.execute(query, {"id": id_gasto})
        if resultado.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return {"mensaje": "Gasto eliminado correctamente"}

