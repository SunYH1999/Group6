import tkinter as tk
from tkinter import ttk
from vendor_management import VendorManager
from product_management import ProductManager
from order_management import OrderManager

class AdminDashboard:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        
        self.window = tk.Toplevel(root)
        self.window.title("Administrator Panel")
        self.window.geometry("300x200")
        
        ttk.Button(self.window, text="Vendor Management", command=self.manage_vendors).pack(pady=10)
        ttk.Button(self.window, text="Product Management", command=self.manage_products).pack(pady=10)
        ttk.Button(self.window, text="Order Management", command=self.manage_orders).pack(pady=10)
    
    def manage_vendors(self):
        VendorManager(self.window, self.db)
    
    def manage_products(self):
        ProductManager(self.window, self.db)
    
    def manage_orders(self):
        OrderManager(self.window, self.db)