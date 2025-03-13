import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog
import mysql.connector


class ProductManager(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Product Management")
        self.geometry("1000x600")

        # Initialize tree attribute
        self.tree = None
        # Initialize button framework properties
        self.btn_frame = None

        # Vendor selection of components
        self.vendor_var = tk.StringVar()
        ttk.Label(self, text="Choose Vendor:").pack(pady=5)
        self.vendor_combobox = ttk.Combobox(self, textvariable=self.vendor_var, state="readonly")
        self.vendor_combobox.pack()
        self.vendor_combobox.bind("<<ComboboxSelected>>", self.load_products)

        # Load vendor data
        self.load_vendors()

    def load_vendors(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT vendor_id, business_name FROM vendors")
        vendors = cursor.fetchall()

        # Handling empty data situations
        if not vendors:
            messagebox.showinfo("Tip", "Please add the vendor first")
            self.destroy()
            return

        self.vendor_combobox["values"] = [f"{vid} - {name}" for vid, name in vendors]
        self.vendor_combobox.current(0)
        self.load_products()  # Ensure the product is loaded for the first time

    def load_products(self, event=None):
        # Clean up old components
        if self.tree:
            self.tree.destroy()
        # Clean up old button frames
        if self.btn_frame:
            self.btn_frame.destroy()

        try:
            vendor_id = self.vendor_combobox.get().split(" - ")[0]
        except (IndexError, AttributeError):
            messagebox.showerror("Error", "Invalid vendor selection")
            return

        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT product_id, name, price, tags 
                FROM products 
                WHERE vendor_id = %s
            """, (vendor_id,))
            products = cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database error", str(err))
            return

        # Create Treeview
        columns = ("ID", "Product name", "Price", "Tag")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Fill in data
        for product in products:
            try:
                tags = ", ".join(json.loads(product[3]))
            except:
                tags = "No tag"
            self.tree.insert("", "end", values=(
                product[0],
                product[1],
                f"¥{product[2]}",
                tags
            ))

        # Create a new operation button framework
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.pack(pady=10)
        ttk.Button(self.btn_frame,
                   text="Add Product",
                   command=lambda: AddProductDialog(self, self.db, vendor_id, self.load_products).show()).pack()


class AddProductDialog(Dialog):
    def __init__(self, parent, db, vendor_id, refresh_callback):
        self.db = db
        self.vendor_id = vendor_id
        super().__init__(parent, "Add Product")
    # Fill in your functional code
    # Admin Panel - Product Management - Product Add