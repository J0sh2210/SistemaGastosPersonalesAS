#/*ELR_ENMA*/
# Gastos Recurrentes API

API para gestionar gastos recurrentes personales con FastAPI y SQL Server.

## 📁 Estructura del Proyecto

```
Proyecto 2026/
│
├── main.py                    # Archivo principal de la aplicación
│
├── app/                       # Paquete de aplicación
│   ├── __init__.py
│   ├── models.py             # Modelos SQLAlchemy
│   ├── schemas.py            # Esquemas Pydantic
│   ├── routes.py             # Rutas/endpoints de la API
│   ├── dependencies.py       # Dependencias (get_db, etc.)
│   │
│   └── models/               # (Opcional) Modelos en carpeta separada
│   └── routes/               # (Opcional) Rutas en carpeta separada
│   └── schemas/              # (Opcional) Esquemas en carpeta separada
│
├── database/                  # Configuración de base de datos
│   ├── __init__.py
│   └── config.py             # Conexión y configuración BD
│
├── sql/                       # Scripts SQL
│   └── SQLQuery1.sql         # Scripts personalizados
│
├── docs/                      # Documentación
│   └── word.docx             # Documentación del proyecto
│
├── .venv/                     # Ambiente virtual
├── .git/                      # Repositorio git
│
└── README.md                  # Este archivo
```

## 🚀 Inicio Rápido

### Activar ambiente virtual
```bash
.venv\Scripts\Activate.ps1
```

### Ejecutar el servidor
```bash
python -m uvicorn main:app --reload
```

El servidor estará disponible en: `http://127.0.0.1:8000`

## 📚 Documentación Interactiva

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📡 Endpoints Principales

### Gastos Recurrentes
- `POST /recurring-expenses` - Crear gasto
- `GET /recurring-expenses` - Listar gastos
- `GET /recurring-expenses/{id}` - Obtener gasto por ID
- `PUT /recurring-expenses/{id}` - Actualizar gasto
- `DELETE /recurring-expenses/{id}` - Eliminar gasto
- `PUT /recurring-expenses/{id}/toggle` - Activar/desactivar gasto

## 🗂️ Descripción de Módulos

### `app/models.py`
Modelos SQLAlchemy que representan las tablas de la base de datos:
- `Cliente` - Información del cliente
- `RecurringExpense` - Gastos recurrentes

### `app/schemas.py`
Esquemas Pydantic para validación de datos:
- `ClienteCreate`, `ClienteRead` - Esquemas de cliente
- `RecurringExpenseCreate`, `RecurringExpenseRead`, `RecurringExpenseUpdate` - Esquemas de gasto

### `app/routes.py`
Definición de todos los endpoints de la API.

### `app/dependencies.py`
Dependencias reutilizables (ej: `get_db()` para acceso a BD).

### `database/config.py`
- Configuración de conexión a SQL Server
- Creación de sesiones
- Inicialización de tablas

## 🔧 Configuración de Base de Datos

La aplicación se conecta a SQL Server en:
```
mssql+pyodbc://@ENMITA\SQLEXPRESS/SistemasGastosAS
```

Modifica en `database/config.py` si necesitas cambiar la conexión.

## 📝 Variables de Entorno (Opcional)

Para mayor seguridad, considera usar variables de entorno:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
```

## ✅ Validaciones

- Montos positivos
- Nombres de gasto con mínimo 1 carácter
- Fechas válidas
- Frecuencias enumeradas (actualmente: "mensual")

## 🛠️ Stack Tecnológico

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **SQL Server** - Base de datos

## 📝 Notas de Desarrollo

- El modo `--reload` detecta cambios automáticamente
- Los logs de SQLAlchemy están habilitados (`echo=True`)
- Usa Swagger UI (`/docs`) para probar endpoints

---

Creado: Abril 2026
