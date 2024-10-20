import tkinter as tk
from tkinter import messagebox
import psycopg2

# Hàm để kết nối với PostgreSQL và kiểm tra thông tin đăng nhập
def check_login():
    username = entry_username.get()
    password = entry_password.get()

    try:
        # Kết nối tới PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="mystore_db",
            user="postgres",          
            password="hathien2003"
        )
        cur = conn.cursor()

        # Thực hiện truy vấn để kiểm tra thông tin đăng nhập
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cur.fetchone()

        if result:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showwarning("Failed", "Invalid username or password!")

        # Đóng kết nối cơ sở dữ liệu
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Hàm để đăng ký người dùng mới
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showwarning("Input Error", "Username and Password cannot be empty!")
        return

    try:
        # Kết nối tới PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="mystore_db",
            user="postgres",          
            password="hathien2003"   # Đổi thành mật khẩu của bạn
        )
        cur = conn.cursor()

        # Kiểm tra xem người dùng đã tồn tại chưa
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if result:
            messagebox.showwarning("Error", "Username already exists!")
        else:
            # Thêm người dùng mới vào cơ sở dữ liệu
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")

        # Đóng kết nối cơ sở dữ liệu
        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Tạo giao diện GUI với Tkinter
root = tk.Tk()
root.title("Login System")

# Giao diện đăng nhập
label_username = tk.Label(root, text="Username:")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Nút đăng nhập
button_login = tk.Button(root, text="Login", command=check_login)
button_login.pack(pady=10)

# Nút đăng ký
button_register = tk.Button(root, text="Register", command=register_user)
button_register.pack(pady=10)

# Chạy giao diện GUI
root.mainloop()
