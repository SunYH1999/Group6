import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from admin_dashboard import AdminDashboard
from customer_dashboard import CustomerDashboard

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-commerce system login")
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="00000000",
            database="GROUP6"
        )
        self.setup_ui()
        
    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0)
        
        ttk.Label(frame, text="Username:").grid(row=0, column=0)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1)
        
        ttk.Label(frame, text="Password:").grid(row=1, column=0)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        self.role_var = tk.StringVar(value="customer")
        ttk.Radiobutton(frame, text="Customer", variable=self.role_var, value="customer").grid(row=2, column=0)
        ttk.Radiobutton(frame, text="Admin", variable=self.role_var, value="admin").grid(row=2, column=1)
        
        ttk.Button(frame, text="Login", command=self.login).grid(row=3, column=0)
        ttk.Button(frame, text="Register", command=self.show_register).grid(row=3, column=1)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        
        cursor = self.db.cursor()
        try:
            if role == "admin":
                query = "SELECT * FROM administrators WHERE username = %s AND password = %s"
            else:
                query = "SELECT * FROM customers WHERE username = %s AND password = %s"
            
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                self.root.withdraw()
                if role == "admin":
                    AdminDashboard(self.root, self.db)
                else:
                    CustomerDashboard(self.root, self.db, user)
            else:
                messagebox.showerror("Error", "Authentication failed")
        finally:
            cursor.close()
    
    def show_register(self):
        if self.role_var.get() == "admin":
            messagebox.showwarning("Error", "Administrator account cannot be registered")
            return
        RegisterWindow(self.root, self.db)

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("Customer Registration")
        
        ttk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1)
        
        ttk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)
        
        ttk.Label(self, text="Contact Number:").grid(row=2, column=0)
        self.contact_entry = ttk.Entry(self)
        self.contact_entry.grid(row=2, column=1)
        
        ttk.Label(self, text="Receiving address:").grid(row=3, column=0)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=3, column=1)
        
        ttk.Button(self, text="Register", command=self.register).grid(row=4, column=0, columnspan=2)
        
    def register(self):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "INSERT INTO customers (username, password, contact_number, shipping_address) VALUES (%s, %s, %s, %s)",
                (
                    self.username_entry.get(),
                    self.password_entry.get(),
                    self.contact_entry.get(),
                    self.address_entry.get()
                )
            )
            self.db.commit()
            messagebox.showinfo("Success", "Registered successfully！")
            self.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Register failed: {err}")
        finally:
            cursor.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()