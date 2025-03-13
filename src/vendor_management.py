import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog
import mysql.connector

class VendorManager(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Verdor Management")
        self.geometry("800x400")
        self.load_vendors()
        
    def load_vendors(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        cursor = self.db.cursor()
        cursor.execute("SELECT vendor_id, business_name, feedback_score, location FROM vendors")
        vendors = cursor.fetchall()
        
        columns = ("ID", "Vendor name", "Rating", "Location")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        for vendor in vendors:
            self.tree.insert("", "end", values=vendor)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh", command=self.load_vendors).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Vendor", command=self.add_vendor).pack(side=tk.LEFT, padx=5)
        
    def add_vendor(self):
        AddVendorDialog(self, self.db).show()

class AddVendorDialog(Dialog):
    def __init__(self, parent, db):
        self.db = db
        super().__init__(parent, "Add Vendor")
    # Fill in your functional code
    # Admin Panel - Vendor Management - Vendor Add