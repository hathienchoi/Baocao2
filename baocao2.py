import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import messagebox, ttk


# Hàm kết nối đến cơ sở dữ liệu
def connect_to_db(username, password):
    try:
        connection = psycopg2.connect(
            dbname="mystore_db",  
            user="postgres",
            password="hathien2003",
            host="localhost"
        )
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        return connection
    except psycopg2.OperationalError as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None


# Chức năng tìm kiếm sản phẩm không phân biệt hoa thường
def search_product(connection, product_name):
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM products WHERE product_name ILIKE %s"
            cursor.execute(query, ('%' + product_name + '%',))
            result = cursor.fetchall()
            return result
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm sản phẩm: {e}")
        return None


# Chức năng thêm sản phẩm mới
def add_product(connection, product_name, product_price, category_id):
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO products (product_name, product_price, category_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (product_name, product_price, category_id))
            connection.commit()
            messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {e}")


# Giao diện đăng nhập
def login_form():
    window = tk.Tk()
    window.title("Đăng Nhập Hệ Thống")
    window.geometry("400x250")
    window.configure(bg="#F0F0F0")

    tk.Label(window, text="Đăng Nhập")

    login_frame = ttk.Frame(window)
    login_frame.pack(pady=10)

    tk.Label(login_frame, text="Tên đăng nhập:")
    username_entry = ttk.Entry(login_frame, width=30)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Mật khẩu:")
    password_entry = ttk.Entry(login_frame, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        if username.strip() == "" or password.strip() == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin!")
        else:
            connection = connect_to_db(username, password)
            if connection:
                window.destroy()
                show_menu(connection)

    window.bind('<Return>', lambda event: login_action())

    ttk.Button(window, text="Đăng Nhập", command=login_action, style='TButton').pack(pady=15)

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=6)
    window.mainloop()


# Ví dụ về chức năng menu sau khi đăng nhập (cần được triển khai)
def show_menu(connection):
    menu_window = tk.Tk()
    menu_window.title("Menu Quản Lý")
    menu_window.geometry("300x200")
    tk.Label(menu_window, text="Chọn chức năng:", font=("Arial", 14)).pack(pady=20)
    
    ttk.Button(menu_window, text="Tìm kiếm sản phẩm", command=lambda: search_product_form(connection)).pack(pady=5)
    ttk.Button(menu_window, text="Thêm sản phẩm", command=lambda: add_product_form(connection)).pack(pady=5)
    
    menu_window.mainloop()


# Giao diện tìm kiếm sản phẩm (cần thêm chi tiết nếu muốn)
def search_product_form(connection):
    search_window = tk.Tk()
    search_window.title("Tìm kiếm sản phẩm")
    search_window.geometry("400x200")
    
    tk.Label(search_window, text="Nhập tên sản phẩm:", font=("Arial", 12)).pack(pady=10)
    search_entry = ttk.Entry(search_window, width=30)
    search_entry.pack(pady=5)
    
    def search_action():
        product_name = search_entry.get()
        result = search_product(connection, product_name)
        if result:
            messagebox.showinfo("Kết quả", f"Tìm thấy {len(result)} sản phẩm.")
    
    ttk.Button(search_window, text="Tìm kiếm", command=search_action).pack(pady=15)
    search_window.mainloop()


# Giao diện thêm sản phẩm (cần thêm chi tiết nếu muốn)
def add_product_form(connection):
    add_window = tk.Tk()
    add_window.title("Thêm sản phẩm mới")
    add_window.geometry("400x300")

    tk.Label(add_window, text="Tên sản phẩm:", font=("Arial", 12)).pack(pady=10)
    product_name_entry = ttk.Entry(add_window, width=30)
    product_name_entry.pack(pady=5)

    tk.Label(add_window, text="Giá sản phẩm:", font=("Arial", 12)).pack(pady=10)
    product_price_entry = ttk.Entry(add_window, width=30)
    product_price_entry.pack(pady=5)

    tk.Label(add_window, text="Mã loại sản phẩm:", font=("Arial", 12)).pack(pady=10)
    category_id_entry = ttk.Entry(add_window, width=30)
    category_id_entry.pack(pady=5)

    def add_action():
        product_name = product_name_entry.get()
        product_price = product_price_entry.get()
        category_id = category_id_entry.get()
        if product_name and product_price and category_id:
            add_product(connection, product_name, float(product_price), int(category_id))

    ttk.Button(add_window, text="Thêm sản phẩm", command=add_action).pack(pady=15)
    add_window.mainloop()

# Khởi chạy giao diện đăng nhập
login_form()
