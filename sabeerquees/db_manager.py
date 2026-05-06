import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'budget_app.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL DEFAULT 'Default User',
            email TEXT UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            UNIQUE(user_id, month, category)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            spent REAL NOT NULL,
            budgeted REAL NOT NULL,
            percentage REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, month, category)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts_seen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, month, category)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            alert_threshold REAL DEFAULT 80
        )
    ''')
    
    cursor.execute('INSERT OR IGNORE INTO config (id, alert_threshold) VALUES (1, 80)')
    cursor.execute('INSERT OR IGNORE INTO users (id, name) VALUES (1, "Default User")')
    
    conn.commit()
    conn.close()

def migrate_json_data(budgets_json, expenses_json, alerts_json, alerts_seen_json, config_json):
    """Migrate existing JSON data to SQLite database"""
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    
    # Migrate config
    threshold = config_json.get('alert_threshold', 80)
    cursor.execute('UPDATE config SET alert_threshold = ? WHERE id = 1', (threshold,))
    
    # Migrate budgets
    for month, categories in budgets_json.items():
        for category, amount in categories.items():
            cursor.execute('''
                INSERT OR REPLACE INTO budgets (user_id, month, category, amount)
                VALUES (1, ?, ?, ?)
            ''', (month, category, amount))
    
    # Migrate expenses
    for month, categories in expenses_json.items():
        for category, amount in categories.items():
            cursor.execute('''
                INSERT INTO expenses (user_id, month, category, amount)
                VALUES (1, ?, ?, ?)
            ''', (month, category, amount))
    
    # Migrate alerts
    for alert_id, alert in alerts_json.items():
        cursor.execute('''
            INSERT OR REPLACE INTO alerts (user_id, month, category, spent, budgeted, percentage, status)
            VALUES (1, ?, ?, ?, ?, ?, ?)
        ''', (alert.get('month'), alert.get('category'), alert.get('spent'), 
              alert.get('budgeted'), alert.get('percentage'), alert.get('status')))
    
    # Migrate alerts_seen
    for key in alerts_seen_json:
        parts = key.split('_')
        if len(parts) >= 2:
            month = parts[0]
            category = '_'.join(parts[1:])
            cursor.execute('''
                INSERT OR IGNORE INTO alerts_seen (user_id, month, category)
                VALUES (1, ?, ?)
            ''', (month, category))
    
    conn.commit()
    conn.close()

def sp_check_budget_alerts(user_id=1, month=None):
    """
    Stored Procedure Simulation:
    Consulta los gastos del usuario en el último mes, calcula el porcentaje 
    vs presupuesto, y genera alertas si se acerca al umbral (80%) o lo excede (100%).
    """
    if month is None:
        month = datetime.now().strftime('%Y-%m')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Obtener umbral de alerta
    cursor.execute('SELECT alert_threshold FROM config WHERE id = 1')
    row = cursor.fetchone()
    threshold = row['alert_threshold'] if row else 80
    
    # SP: Consultar últimos movimientos del mes y calcular porcentaje
    cursor.execute('''
        SELECT 
            b.category,
            b.amount as budgeted,
            COALESCE(SUM(e.amount), 0) as spent
        FROM budgets b
        LEFT JOIN expenses e ON b.user_id = e.user_id 
            AND b.month = e.month 
            AND b.category = e.category
        WHERE b.user_id = ? AND b.month = ?
        GROUP BY b.category, b.amount
    ''', (user_id, month))
    
    results = cursor.fetchall()
    alerts_triggered = []
    
    for row in results:
        budgeted = row['budgeted']
        spent = row['spent']
        percentage = (spent / budgeted * 100) if budgeted > 0 else 0
        
        if percentage > 100:
            status = 'exceeded'
        elif percentage >= threshold:
            status = 'warning'
        else:
            status = 'ok'
        
        if status in ['warning', 'exceeded']:
            # Verificar si ya existe alerta para este mes/categoría/usuario (no duplicados)
            cursor.execute('''
                SELECT id FROM alerts 
                WHERE user_id = ? AND month = ? AND category = ?
            ''', (user_id, month, row['category']))
            
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO alerts (user_id, month, category, spent, budgeted, percentage, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, month, row['category'], spent, budgeted, round(percentage, 2), status))
                alerts_triggered.append({
                    'category': row['category'],
                    'spent': spent,
                    'budgeted': budgeted,
                    'percentage': round(percentage, 2),
                    'status': status
                })
    
    conn.commit()
    conn.close()
    return alerts_triggered

