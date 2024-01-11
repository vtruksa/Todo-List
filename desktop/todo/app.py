import tkinter as tk
from tkinter import ttk

import settings
import sqlite3

from passwords import checkPassword

class App:
    def __init__(self, root):
        self.root = root
        print(settings.DB_PATH)
        self.db_conn = sqlite3.connect(settings.DB_PATH)
        self.db_cursor = self.db_conn.cursor()
        self.loginWin()

    def loginWin(self):
        win = tk.Toplevel(self.root)
        win.title("Login")
        
        lab_username = tk.Label(win, text="Username: ")
        lab_username.grid(row=0, column=0, padx=5, pady=5)

        username = tk.Entry(win)
        username.grid(row=0, column=1, padx=5, pady=5)

        lab_pass = tk.Label(win, text="Password: ")
        lab_pass.grid(row=1, column=0, padx=5, pady=5)

        password = tk.Entry(win, show="*")
        password.grid(row=1, column=1, padx=5, pady=5)

        btn = tk.Button(win, text="Login", command=lambda: self.login(win, username, password))
        btn.grid(row = 2, columnspan=2, padx=5, pady=5)

        win.mainloop()

    def login(self, win, username, password):
        u = username.get()
        p = password.get()

        self.db_cursor.execute(f"""
            SELECT id, username, password
            FROM auth_user
            WHERE username = '{u}'
        """)

        user = self.db_cursor.fetchone()

        if checkPassword(p, user[2]):
            self.user = user
            win.destroy()
        else:
            win.destroy()
            self.loginWin()