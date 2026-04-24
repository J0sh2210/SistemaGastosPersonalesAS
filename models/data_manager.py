import json
import os
from datetime import datetime
from database.db_manager import get_db, init_db, migrate_json_data, sp_check_budget_alerts

class DataManager:
    def __init__(self, base_path='.'):
        self.base_path = base_path
        init_db()
        
        # Migrate existing JSON data on first run if DB is empty
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM budgets')
        if cursor.fetchone()['count'] == 0:
            budgets = self._load_json('budgets.json')
            expenses = self._load_json('expenses.json')
            alerts = self._load_json('alerts.json')
            alerts_seen = self._load_json('alerts_seen.json')
            config = self._load_json('config.json')
            migrate_json_data(budgets, expenses, alerts, alerts_seen, config)
        conn.close()

    def _load_json(self, filename):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def get_current_month(self):
        return datetime.now().strftime('%Y-%m')

    def get_threshold(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT alert_threshold FROM config WHERE id = 1')
        row = cursor.fetchone()
        conn.close()
        return row['alert_threshold'] if row else 80

    def set_threshold(self, threshold):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE config SET alert_threshold = ? WHERE id = 1', (float(threshold),))
        conn.commit()
        conn.close()

    def add_budget(self, month, category, amount, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO budgets (user_id, month, category, amount)
            VALUES (?, ?, ?, ?)
        ''', (user_id, month, category, float(amount)))
        conn.commit()
        conn.close()

    def add_expense(self, month, category, amount, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, month, category, amount)
            VALUES (?, ?, ?, ?)
        ''', (user_id, month, category, float(amount)))
        conn.commit()
        conn.close()
        
        # Ejecutar SP para verificar alertas después de agregar gasto
        alerts = sp_check_budget_alerts(user_id, month)
        
        # Retornar True si se generó alerta para la categoría agregada
        for alert in alerts:
            if alert['category'] == category:
                return True
        return False

    def get_categories_data(self, month, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT alert_threshold FROM config WHERE id = 1')
        row = cursor.fetchone()
        threshold = row['alert_threshold'] if row else 80
        
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
        
        rows = cursor.fetchall()
        conn.close()
        
        categories = {}
        for row in rows:
            budgeted = row['budgeted']
            spent = row['spent']
            percentage = (spent / budgeted * 100) if budgeted > 0 else 0
            status = 'exceeded' if percentage > 100 else 'warning' if percentage >= threshold else 'ok'
            categories[row['category']] = {
                'budgeted': budgeted,
                'spent': spent,
                'percentage': round(percentage, 2),
                'status': status
            }
        return categories

    def _check_alerts(self, month, user_id=1):
        """Legacy method - now uses SP"""
        alerts = sp_check_budget_alerts(user_id, month)
        return len(alerts) > 0

    def clear_alert(self, month, category, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM alerts_seen 
            WHERE user_id = ? AND month = ? AND category = ?
        ''', (user_id, month, category))
        conn.commit()
        conn.close()

    def reset_data(self, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM alerts_seen WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM alerts WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

    def get_alerts_data(self, month: str = None, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        if month:
            cursor.execute('''
                SELECT * FROM alerts 
                WHERE user_id = ? AND month = ?
                ORDER BY created_at DESC
            ''', (user_id, month))
        else:
            cursor.execute('''
                SELECT * FROM alerts 
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_alert(self, alert_id: str):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alerts WHERE id = ?', (alert_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def create_alert(self, alert_id: str, alert_data: dict):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO alerts (id, user_id, month, category, spent, budgeted, percentage, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert_id,
            alert_data.get('user_id', 1),
            alert_data.get('month'),
            alert_data.get('category'),
            alert_data.get('spent'),
            alert_data.get('budgeted'),
            alert_data.get('percentage'),
            alert_data.get('status')
        ))
        conn.commit()
        conn.close()

    def update_alert(self, alert_id: str, alert_data: dict):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM alerts WHERE id = ?', (alert_id,))
        if not cursor.fetchone():
            conn.close()
            return None
        
        cursor.execute('''
            UPDATE alerts SET 
                month = ?, category = ?, spent = ?, budgeted = ?, 
                percentage = ?, status = ?
            WHERE id = ?
        ''', (
            alert_data.get('month'),
            alert_data.get('category'),
            alert_data.get('spent'),
            alert_data.get('budgeted'),
            alert_data.get('percentage'),
            alert_data.get('status'),
            alert_id
        ))
        conn.commit()
        conn.close()
        return alert_data

    def delete_alert(self, alert_id: str):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM alerts WHERE id = ?', (alert_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        cursor.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
        conn.commit()
        conn.close()
        return True

    def get_alerts_by_month_category(self, month: str, category: str, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM alerts 
            WHERE user_id = ? AND month = ? AND category = ?
        ''', (user_id, month, category))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def budget_exists(self, month, category, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM budgets 
            WHERE user_id = ? AND month = ? AND category = ?
        ''', (user_id, month, category))
        row = cursor.fetchone()
        conn.close()
        return row is not None

    def mark_alert_seen(self, month, category, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO alerts_seen (user_id, month, category)
            VALUES (?, ?, ?)
        ''', (user_id, month, category))
        conn.commit()
        conn.close()

    def is_alert_seen(self, month, category, user_id=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM alerts_seen 
            WHERE user_id = ? AND month = ? AND category = ?
        ''', (user_id, month, category))
        row = cursor.fetchone()
        conn.close()
        return row is not None

    def get_new_alerts(self, month, user_id=1):
        """Get alerts not yet seen by user"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.* FROM alerts a
            LEFT JOIN alerts_seen s ON a.user_id = s.user_id 
                AND a.month = s.month AND a.category = s.category
            WHERE a.user_id = ? AND a.month = ? AND s.id IS NULL
        ''', (user_id, month))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

