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

    # def load_orders(self):
    # Admin Panel - Order Management - Order List
    # Fill in your functional code
        

    # def ship_order(self, event):
    # Admin Panel - Order Management - Order shipment
    # Fill in your functional code