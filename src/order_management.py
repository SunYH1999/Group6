import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class OrderManager(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Order Management")
        self.geometry("1200x600")
        self.load_orders()

    def load_orders(self):
        for widget in self.winfo_children():
            widget.destroy()

        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.order_id, c.username, o.order_date, o.status 
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
        """)
        orders = cursor.fetchall()

        columns = ("Order ID", "Customer name", "Order time", "State", "Handle")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

        for order in orders:
            self.tree.insert("", "end", values=(
                order["order_id"],
                order["username"],
                order["order_date"].strftime("%Y-%m-%d %H:%M:%S"),
                order["status"],
                "✓" if order["status"] == "shipped" else "Mark shipment"
            ), tags=(order["status"],))

        self.tree.tag_configure("pending", foreground="red")
        self.tree.bind("<Double-1>", self.ship_order)

    def ship_order(self, event):
        item = self.tree.selection()[0]
        status = self.tree.item(item, "tags")[0]
        if status == "pending":
            order_id = self.tree.item(item, "values")[0]
            if messagebox.askyesno("Confirm", "Are you sure you want to mark it as shipped?"):
                cursor = self.db.cursor()
                cursor.execute("UPDATE orders SET status = 'shipped' WHERE order_id = %s", (order_id,))
                self.db.commit()
                self.load_orders()