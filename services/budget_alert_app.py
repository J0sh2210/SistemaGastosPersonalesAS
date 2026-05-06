import tkinter as tk
from tkinter import ttk, messagebox
from models.data_manager import DataManager
from datetime import datetime

class BudgetAlertApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alerta de Presupuesto")
        self.root.geometry("800x600")

        self.dm = DataManager()
        self.current_month = self.dm.get_current_month()

        self.setup_ui()
        self.refresh_display()

    def setup_ui(self):
        # Config frame
        config_frame = ttk.Frame(self.root)
        config_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(config_frame, text="Umbral de Alerta (%):").pack(side='left')
        self.threshold_var = tk.StringVar(value=str(self.dm.get_threshold()))
        threshold_entry = ttk.Entry(config_frame, textvariable=self.threshold_var, width=5)
        threshold_entry.pack(side='left', padx=5)
        ttk.Button(config_frame, text="Actualizar", command=self.update_threshold).pack(side='left', padx=5)

        ttk.Button(config_frame, text="Reiniciar Datos", command=self.reset_data).pack(side='right')

        # Month selector
        month_frame = ttk.Frame(self.root)
        month_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(month_frame, text="Mes:").pack(side='left')
        self.month_var = tk.StringVar(value=self.current_month)
        month_combo = ttk.Combobox(month_frame, textvariable=self.month_var, values=list(self.dm.budgets.keys()) + [self.current_month], width=10)
        month_combo.pack(side='left', padx=5)
        ttk.Button(month_frame, text="Mes Actual", command=self.set_current_month).pack(side='left', padx=5)
        ttk.Button(month_frame, text="Refrescar", command=self.refresh_display).pack(side='right')

        # Input frames
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill='x', padx=10, pady=5)

        # Add budget
        ttk.Label(input_frame, text="Agregar Presupuesto - Categoría:").grid(row=0, column=0, sticky='w')
        self.budget_cat = ttk.Entry(input_frame, width=15)
        self.budget_cat.grid(row=0, column=1, padx=5)
        ttk.Label(input_frame, text="Monto:").grid(row=0, column=2, sticky='w')
        self.budget_amt = ttk.Entry(input_frame, width=10)
        self.budget_amt.grid(row=0, column=3, padx=5)
        ttk.Button(input_frame, text="Agregar", command=self.add_budget).grid(row=0, column=4, padx=5)

        # Add expense
        ttk.Label(input_frame, text="Agregar Gasto - Categoría:").grid(row=1, column=0, sticky='w')
        self.expense_cat = ttk.Entry(input_frame, width=15)
        self.expense_cat.grid(row=1, column=1, padx=5)
        ttk.Label(input_frame, text="Monto:").grid(row=1, column=2, sticky='w')
        self.expense_amt = ttk.Entry(input_frame, width=10)
        self.expense_amt.grid(row=1, column=3, padx=5)
        ttk.Button(input_frame, text="Agregar", command=self.add_expense_gui).grid(row=1, column=4, padx=5)

        # Categories list
        self.list_frame = ttk.Frame(self.root)
        self.list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Scrollbar
        self.tree = ttk.Treeview(self.list_frame, columns=('Category', 'Budgeted', 'Spent', 'Percentage', 'Status'), show='headings', height=15)
        self.tree.heading('Category', text='Categoría')
        self.tree.heading('Budgeted', text='Presupuestado')
        self.tree.heading('Spent', text='Gastado')
        self.tree.heading('Percentage', text='%')
        self.tree.heading('Status', text='Estado')
        self.tree.column('Category', width=150)
        self.tree.column('Budgeted', width=100)
        self.tree.column('Spent', width=100)
        self.tree.column('Percentage', width=80)
        self.tree.column('Status', width=100)

        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def refresh_display(self):
        month = self.month_var.get()
        categories = self.dm.get_categories_data(month)

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        for cat, data in categories.items():
            status_color = {'ok': 'green', 'warning': 'orange', 'exceeded': 'red'}
            tag = data['status']
            self.tree.insert('', 'end', values=(cat, f"${data['budgeted']:.2f}", f"${data['spent']:.2f}", f"{data['percentage']}%", data['status']), tags=(tag,))
            self.tree.tag_configure('exceeded', background='lightcoral')
            self.tree.tag_configure('warning', background='lightyellow')
            self.tree.tag_configure('ok', background='lightgreen')

    def add_budget(self):
        cat = self.budget_cat.get().strip()
        try:
            amt = float(self.budget_amt.get())
            if cat and amt > 0:
                self.dm.add_budget(self.month_var.get(), cat, amt)
                self.budget_cat.delete(0, tk.END)
                self.budget_amt.delete(0, tk.END)
                self.refresh_display()
                messagebox.showinfo("Éxito", f"Presupuesto agregado: {cat} - ${amt}")
            else:
                messagebox.showerror("Error", "Categoría y monto válido requeridos.")
        except ValueError:
            messagebox.showerror("Error", "Monto debe ser número.")

    def add_expense_gui(self):
        cat = self.expense_cat.get().strip()
        try:
            amt = float(self.expense_amt.get())
            if cat and amt > 0:
                self.dm.add_expense(self.month_var.get(), cat, amt)
                self.expense_cat.delete(0, tk.END)
                self.expense_amt.delete(0, tk.END)
                self.refresh_display()
                # Alert handled in data_manager
                messagebox.showinfo("Éxito", f"Gasto agregado: {cat} - ${amt}")
            else:
                messagebox.showerror("Error", "Categoría y monto válido requeridos.")
        except ValueError:
            messagebox.showerror("Error", "Monto debe ser número.")

    def update_threshold(self):
        try:
            threshold = float(self.threshold_var.get())
            if 0 < threshold < 100:
                self.dm.set_threshold(threshold)
                self.refresh_display()
                messagebox.showinfo("Éxito", f"Umbral actualizado a {threshold}%")
            else:
                messagebox.showerror("Error", "Umbral entre 0 y 100.")
        except ValueError:
            messagebox.showerror("Error", "Porcentaje válido requerido.")

    def set_current_month(self):
        self.month_var.set(self.dm.get_current_month())
        self.refresh_display()

    def reset_data(self):
        if messagebox.askyesno("Confirmar", "¿Reiniciar gastos y alertas?"):
            self.dm.reset_data()
            self.refresh_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetAlertApp(root)
    root.mainloop()
