import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import Dialog
import mysql.connector

class ProductManager(tk.Toplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("产品管理")
        self.geometry("1000x600")
        
        # 初始化 tree 属性
        self.tree = None
        
        # 供应商选择组件
        self.vendor_var = tk.StringVar()
        ttk.Label(self, text="选择供应商:").pack(pady=5)
        self.vendor_combobox = ttk.Combobox(self, textvariable=self.vendor_var, state="readonly")
        self.vendor_combobox.pack()
        self.vendor_combobox.bind("<<ComboboxSelected>>", self.load_products)
        
        # 加载供应商数据
        self.load_vendors()

    def load_vendors(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT vendor_id, business_name FROM vendors")
        vendors = cursor.fetchall()
        
        # 处理空数据情况
        if not vendors:
            messagebox.showinfo("提示", "请先添加供应商")
            self.destroy()
            return
            
        self.vendor_combobox["values"] = [f"{vid} - {name}" for vid, name in vendors]
        self.vendor_combobox.current(0)
        self.load_products()  # 确保首次加载产品

    def load_products(self, event=None):
        # 清理旧组件
        if self.tree:
            self.tree.destroy()
            
        try:
            vendor_id = self.vendor_combobox.get().split(" - ")[0]
        except (IndexError, AttributeError):
            messagebox.showerror("错误", "无效的供应商选择")
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
            messagebox.showerror("数据库错误", str(err))
            return

        # 创建 Treeview
        columns = ("ID", "产品名称", "价格", "标签")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 填充数据
        for product in products:
            try:
                tags = ", ".join(eval(product[3]))
            except:
                tags = "无标签"
            self.tree.insert("", "end", values=(
                product[0],
                product[1],
                f"¥{product[2]}",
                tags
            ))

        # 操作按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, 
                  text="新增产品",
                  command=lambda: AddProductDialog(self, self.db, vendor_id).show()).pack()

class AddProductDialog(Dialog):
    def __init__(self, parent, db, vendor_id):
        self.db = db
        self.vendor_id = vendor_id
        super().__init__(parent, "Add Product")
    # Fill in your functional code
    # Admin Panel - Product Management - Product Add