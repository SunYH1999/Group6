import json
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class ProductBrowser(tk.Toplevel):
    def __init__(self, parent, db, user):
        super().__init__(parent)
        self.db = db
        self.user = user  # user[0] is customer_id
        self.title("Browse products")
        self.geometry("1000x600")

        # Search
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)

        ttk.Label(search_frame, text="Search tags:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.load_products).pack(side=tk.LEFT)

        # Product List
        self.tree = ttk.Treeview(self, columns=("ID", "Product name", "Price", "Vendor", "Tags", "Rating"), show="headings")
        for col in ("ID", "Product name", "Price", "Vendor", "Tags", "Rating"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
            
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(self, text="Purchase the selected product", command=self.purchase_product).pack(pady=10)
        ttk.Button(btn_frame, text="Rate the selected product", command=self.rate_selected_product).pack(side=tk.LEFT, padx=5)

        self.load_products()

    def load_products(self):
        # 清空原有数据
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT p.product_id, p.name, p.price, p.tags, v.business_name, AVG(r.score) as avg_score
            FROM products p
            JOIN vendors v ON p.vendor_id = v.vendor_id
            LEFT JOIN ratings r ON p.product_id = r.product_id
            WHERE %s = '' OR JSON_CONTAINS(p.tags, %s)
            GROUP BY p.product_id
        """
        search_tag = self.search_entry.get().strip()
        params = (search_tag, f'"{search_tag}"') if search_tag else ('', '[]')

        cursor.execute(query, params)
        products = cursor.fetchall()

        for product in products:
            tags = ", ".join(eval(product["tags"]))
            score = f"{product['avg_score']:.1f}" if product['avg_score'] else "暂无评分"
            self.tree.insert("", "end", values=(
                product["product_id"],
                product["name"],
                f"¥{product['price']}",
                product["business_name"],
                tags,
                score
            ))

    def purchase_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Tip", "Please select at least one product first")
            return

        # Get all selected product information
        products = []
        total_amount = 0.0
        for item in selected:
            print(item)
            values = self.tree.item(item, "values")
            try:
                product_id = int(values[0])
                price = float(values[2].replace("¥", ""))
                
                # Get vendor ID
                cursor = self.db.cursor()
                cursor.execute("SELECT vendor_id FROM products WHERE product_id = %s", (product_id,))
                if (vendor_id := cursor.fetchone()):
                    products.append({
                        "product_id": product_id,
                        "vendor_id": vendor_id[0],
                        "price": price
                    })
                    total_amount += price
                else:
                    messagebox.showwarning("Warn", f"Product ID {product_id} is invalid, skipped")
            except Exception as e:
                messagebox.showwarning("Data error", f"Failed to parse product data: {str(e)}")
                continue

        if not products:
            return

        # Confirm Dialog
        if not messagebox.askyesno("Confirm purchase", 
                                 f"Purchase {len(products)} items\nTotal amount: ¥{total_amount:.2f}\nAre you sure to continue?"):
            return

        # Database transactions
        try:
            cursor = self.db.cursor()
            
            # Create order
            cursor.execute(
                "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
                (self.user[0], total_amount))
            order_id = cursor.lastrowid
            
            # Insert order details
            for p in products:
                cursor.execute(
                    """INSERT INTO order_details 
                       (order_id, product_id, vendor_id, quantity)
                       VALUES (%s, %s, %s, 1)""",
                    (order_id, p["product_id"], p["vendor_id"]))
            
            self.db.commit()
            messagebox.showinfo("Success", 
                               f"Order creation successful!\nOrder No: {order_id}\nTotal amount: ¥{total_amount:.2f}")
        except Exception as e:
            self.db.rollback()
            messagebox.showerror("Error", f"Purchase failed: {str(e)}")
        finally:
            cursor.close()


    def rate_product(self, product_id):
        rate_window = tk.Toplevel(self)
        rate_window.title("产品评分")

        ttk.Label(rate_window, text="请选择评分（1 - 5 星）:").pack(pady=10)
        rating_var = tk.IntVar()
        for i in range(1, 6):
            ttk.Radiobutton(rate_window, text=str(i), variable=rating_var, value=i).pack(side=tk.LEFT, padx=5)

        def submit_rating():
            rating = rating_var.get()
            cursor = self.db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO ratings (customer_id, product_id, score) VALUES (%s, %s, %s) "
                    "ON DUPLICATE KEY UPDATE score = %s",
                    (self.user[0], product_id, rating, rating)
                )
                self.db.commit()
                messagebox.showinfo("成功", "评分提交成功！")
                rate_window.destroy()
                self.load_products()
            except mysql.connector.Error as err:
                messagebox.showerror("错误", f"评分提交失败: {err}")

        ttk.Button(rate_window, text="提交评分", command=submit_rating).pack(pady=20)
    def rate_selected_product(self):
        """处理评分按钮点击"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一个商品")
            return
        if len(selected) > 1:
            messagebox.showwarning("提示", "每次只能为一个商品评分")
            return
            
        product_id = self.tree.item(selected[0], "values")[0]
        self.rate_product(product_id)

    def rate_product(self, product_id):
        rate_window = tk.Toplevel(self)
        rate_window.title(f"Rate the product {product_id}")

        # 获取历史评分
        cursor = self.db.cursor()
        cursor.execute("SELECT score FROM ratings WHERE customer_id = %s AND product_id = %s",
                     (self.user[0], product_id))
        history_score = cursor.fetchone()
        
        ttk.Label(rate_window, text="Please choose a rating (1-5 stars):").pack(pady=10)
        rating_var = tk.IntVar(value=history_score[0] if history_score else 3)
        
        # Rating options
        rating_frame = ttk.Frame(rate_window)
        rating_frame.pack()
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, text="★"*i, 
                          variable=rating_var, 
                          value=i).pack(side=tk.LEFT, padx=5)

        def submit_rating():
            try:
                cursor = self.db.cursor()
                cursor.execute(
                    """INSERT INTO ratings (customer_id, product_id, score)
                       VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE score = VALUES(score)""",
                    (self.user[0], product_id, rating_var.get()))
                self.db.commit()
                messagebox.showinfo("Success", "The rating has been updated!")
                rate_window.destroy()
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", f"Rating failed: {str(e)}")
                self.db.rollback()

        ttk.Button(rate_window, text="Submit", command=submit_rating).pack(pady=10)

