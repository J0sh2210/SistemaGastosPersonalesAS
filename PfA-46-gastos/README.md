# PfA-46 — Registro y Edición de Gastos

API FastAPI para registrar y editar gastos personales, persistiendo los datos en SQL Server.

## Endpoints principales

- `POST /gastos` — Registrar un nuevo gasto.
- `PUT /gastos/{id}` — Editar un gasto existente.
- `GET /gastos` — Listar todos los gastos.
- `GET /gastos/{id}` — Consultar un gasto por ID.
- `DELETE /gastos/{id}` — Eliminar un gasto.

## Requisitos

- Python 3.10+
- SQL Server con las tablas `Movimiento`, `Cliente` y `CategoriaMovimiento`.

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con:

```env
DB_CadenaConection=mssql+pyodbc://usuario:password@servidor/bd?driver=ODBC+Driver+17+for+SQL+Server
```

## Ejecución

```bash
uvicorn main:app --reload
```

