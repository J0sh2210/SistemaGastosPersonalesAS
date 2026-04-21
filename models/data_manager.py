import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, base_path='.'):  # Use current working directory
        self.base_path = base_path
        self.config = self._load_json('config.json')
        self.budgets = self._load_json('budgets.json')
        self.expenses = self._load_json('expenses.json')
        self.alerts_seen = self._load_json('alerts_seen.json')

    def _load_json(self, filename):
        path = os.path.join(self.base_path, filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def _save_json(self, filename, data):
        path = os.path.join(self.base_path, filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_current_month(self):
        return datetime.now().strftime('%Y-%m')

    def get_threshold(self):
        return self.config.get('alert_threshold', 80)

    def set_threshold(self, threshold):
        self.config['alert_threshold'] = float(threshold)
        self._save_json('config.json', self.config)

    def add_budget(self, month, category, amount):
        if month not in self.budgets:
            self.budgets[month] = {}
        self.budgets[month][category] = float(amount)
        self._save_json('budgets.json', self.budgets)

    def add_expense(self, month, category, amount):
        if month not in self.expenses:
            self.expenses[month] = {}
        if category not in self.expenses[month]:
            self.expenses[month][category] = 0.0
        self.expenses[month][category] += float(amount)
        self._save_json('expenses.json', self.expenses)
        # Check for alert after adding
        self._check_alerts(month)

    def get_categories_data(self, month):
        categories = {}
        if month in self.budgets:
            for cat, budgeted in self.budgets[month].items():
                spent = self.expenses.get(month, {}).get(cat, 0.0)
                percentage = (spent / budgeted * 100) if budgeted > 0 else 0
                status = 'exceeded' if percentage > 100 else 'warning' if percentage >= self.get_threshold() else 'ok'
                categories[cat] = {
                    'budgeted': budgeted,
                    'spent': spent,
                    'percentage': round(percentage, 2),
                    'status': status
                }
        return categories

    def _check_alerts(self, month):
        categories_data = self.get_categories_data(month)
        for cat, data in categories_data.items():
            key = f"{month}_{cat}"
            if key not in self.alerts_seen:
                if data['status'] == 'warning' or data['status'] == 'exceeded':
                    self.alerts_seen[key] = True
                    self._save_json('alerts_seen.json', self.alerts_seen)
                    return True  # Alert needed
        return False

    def clear_alert(self, month, category):
        key = f"{month}_{category}"
        if key in self.alerts_seen:
            del self.alerts_seen[key]
            self._save_json('alerts_seen.json', self.alerts_seen)

    def reset_data(self):
        self.expenses = {}
        self.alerts_seen = {}
        self._save_json('expenses.json', self.expenses)
        self._save_json('alerts_seen.json', self.alerts_seen)

