import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class OrderViewer(tk.Toplevel):
    def __init__(self, parent, db, user):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.title("My Order")
        self.geometry("1200x600")

        # 订单列表
        columns = ("Order ID", "Order time", "State", "Total amount", "Handle")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind Double Click Event
        self.tree.bind("<Double-1>", self.show_order_details)

        self.load_orders()

    def load_orders(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.order_id, o.order_date, o.status,
                   SUM(p.price) AS total
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN products p ON od.product_id = p.product_id
            WHERE o.customer_id = %s
            GROUP BY o.order_id
        """, (self.user[0],))

        orders = cursor.fetchall()
        for order in orders:
            self.tree.insert("", "end", values=(
                order["order_id"],
                order["order_date"].strftime("%Y-%m-%d %H:%M:%S"),
                order["status"],
                f"¥{order['total']}",
                "Delete" if order["status"] == "pending" else ""
            ), tags=(order["status"],))

        self.tree.tag_configure("pending", foreground="red")

    def show_order_details(self, event):
        item = self.tree.selection()[0]
        order_id = self.tree.item(item, "values")[0]
        status = self.tree.item(item, "tags")[0]

        details_window = tk.Toplevel(self)
        details_window.title(f"Order details - Order No. {order_id}")

        # 显示订单商品
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.name, p.price, v.business_name 
            FROM order_details od
            JOIN products p ON od.product_id = p.product_id
            JOIN vendors v ON od.vendor_id = v.vendor_id
            WHERE od.order_id = %s
        """, (order_id,))

        products = cursor.fetchall()

        for i, product in enumerate(products):
            ttk.Label(details_window, text=f"{i+1}. {product['name']} - ¥{product['price']} ({product['business_name']})").pack(anchor=tk.W)

        # Add and delete button
        if status == "pending":
            ttk.Button(details_window, 
                      text="Delete Order",
                      command=lambda: self.delete_order(order_id)).pack(pady=10)

    def delete_order(self, order_id):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this order?"):
            cursor = self.db.cursor()
            try:
                cursor.execute("DELETE FROM order_details WHERE order_id = %s", (order_id,))
                cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
                self.db.commit()
                self.load_orders()
                messagebox.showinfo("Success", "Order has been deleted")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Delete failed: {err}")