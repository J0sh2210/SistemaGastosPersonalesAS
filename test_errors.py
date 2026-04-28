#!/usr/bin/env python
"""Script para identificar errores en el proyecto"""

import sys

print("=== Test 1: Import main_fixed ===")
try:
    from routes.main_fixed import app
    print("OK: main_fixed importa correctamente")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n=== Test 2: Pydantic v2 .dict() vs .model_dump() ===")
try:
    from registro.alerta.models.alert_model import AlertUpdate
    update = AlertUpdate(spent=100)
    # Test .dict() (Pydantic v1 style - should fail or warn in v2)
    try:
        result = update.dict(exclude_unset=True)
        print(f"WARN: .dict() funcionó pero está deprecado: {result}")
    except AttributeError as e:
        print(f"ERROR: .dict() falló en Pydantic v2: {e}")
    # Test .model_dump() (Pydantic v2 style)
    try:
        result = update.model_dump(exclude_unset=True)
        print(f"OK: .model_dump() funciona: {result}")
    except AttributeError as e:
        print(f"ERROR: .model_dump() no existe: {e}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n=== Test 3: SQLite schema - insert string ID into INTEGER PK ===")
try:
    import sqlite3
    import os
    DB_PATH = os.path.join(os.path.dirname(__file__), 'budget_app.db')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Try inserting a string ID into alerts table
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO alerts (id, user_id, month, category, spent, budgeted, percentage, status)
            VALUES (?, 1, '2024-10', 'Test', 100, 200, 50.0, 'ok')
        ''', ("2024-10_Test_20240101_120000",))
        conn.commit()
        print("OK: String ID insertado (SQLite permitió)")
    except sqlite3.IntegrityError as e:
        print(f"ERROR IntegrityError: {e}")
    except sqlite3.DataError as e:
        print(f"ERROR DataError: {e}")
    except Exception as e:
        print(f"ERROR {type(e).__name__}: {e}")
    
    conn.close()
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n=== Test 4: DataManager.budgets attribute ===")
try:
    from models.data_manager import DataManager
    dm = DataManager()
    try:
        budgets = dm.budgets
        print(f"OK: dm.budgets existe: {budgets}")
    except AttributeError as e:
        print(f"ERROR: dm.budgets no existe: {e}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n=== Test 5: AlertService create_alert ===")
try:
    from models.data_manager import DataManager
    from registro.alerta.models.alert_model import AlertCreate
    from registro.alerta.services.alert_service import create_alert
    
    dm = DataManager()
    alert_data = AlertCreate(
        month="2024-10",
        category="TestCat",
        spent=100,
        budgeted=200,
        percentage=50.0,
        status="ok"
    )
    alert_id = create_alert(dm, alert_data)
    print(f"OK: Alerta creada con ID: {alert_id}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n=== Test 6: GET /alertas/{month} response model ===")
try:
    from models.data_manager import DataManager
    from registro.alerta.models.alert_model import AlertResponse
    dm = DataManager()
    alerts = dm.get_alerts_data("2024-10")
    print(f"Alertas encontradas: {len(alerts)}")
    for alert in alerts:
        print(f"  Alert raw: {alert}")
        try:
            ar = AlertResponse(**alert)
            print(f"  OK: AlertResponse creado: id={ar.id}, created_at={ar.created_at}")
        except Exception as e:
            print(f"  ERROR validación AlertResponse: {type(e).__name__}: {e}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

print("\n=== Resumen ===")
print("Revisa los errores arriba para entender qué falla.")

