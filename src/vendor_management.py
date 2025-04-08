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
        self.cursor = db.cursor()  # Create cursor during initialization
        super().__init__(parent, "Add Vendor")

    def body(self, master):
        # Add labels and input fields
        ttk.Label(master, text="Business Name:").grid(row=0, column=0)
        self.business_name_entry = ttk.Entry(master)
        self.business_name_entry.grid(row=0, column=1)

        ttk.Label(master, text="Location:").grid(row=1, column=0)
        self.location_entry = ttk.Entry(master)
        self.location_entry.grid(row=1, column=1)

        # Set initial focus
        return self.business_name_entry

    def validate(self):
        # Get user input
        business_name = self.business_name_entry.get().strip()
        location = self.location_entry.get().strip()

        # Check if input is empty
        if not business_name or not location:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return False

        # Check if business name is valid
        if not business_name.replace(" ", "").isalnum():
            messagebox.showwarning("Input Error", "Business name contains invalid characters")
            return False

        # Check for duplicate business name
        try:
            self.cursor.execute(
                "SELECT business_name FROM vendors WHERE business_name = %s",
                (business_name,)
            )
            if self.cursor.fetchone():
                messagebox.showwarning("Duplicate Name", "A vendor with this name already exists!")
                return False
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to check vendor name: {err}")
            return False

        return True

    def apply(self):
        # Get user input
        business_name = self.business_name_entry.get().strip()
        location = self.location_entry.get().strip()

        # Insert data into database
        try:
            self.cursor.execute(
                "INSERT INTO vendors (business_name, location) VALUES (%s, %s)",
                (business_name, location)
            )
            self.db.commit()
            messagebox.showinfo("Success", "Vendor added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add vendor: {err}")
        finally:
            self.cursor.close()

    def destroy(self):
        # Close the cursor when the dialog is destroyed
        if self.cursor:
            self.cursor.close()
        super().destroy()