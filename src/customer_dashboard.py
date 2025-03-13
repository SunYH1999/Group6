import tkinter as tk
from tkinter import ttk
from product_browser import ProductBrowser
from order_viewer import OrderViewer

class CustomerDashboard:
    def __init__(self, root, db, user):
        self.root = root
        self.db = db
        self.user = user
        
        self.window = tk.Toplevel(root)
        self.window.title("Customer Panel")
        self.window.geometry("300x150")
        
        ttk.Button(self.window, text="Browse Products", command=self.browse_products).pack(pady=10)
        ttk.Button(self.window, text="My Order", command=self.view_orders).pack(pady=10)
    
    def browse_products(self):
        ProductBrowser(self.window, self.db, self.user)
    
    def view_orders(self):
        OrderViewer(self.window, self.db, self.user)