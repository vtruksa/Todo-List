import tkinter as tk
from tkinter import ttk

import settings
import sqlite3

class App:
    def __init__(self, root):
        self.root = root
        print(settings.DB_PATH)
        self.db_conn = sqlite3.connect(settings.DB_PATH)
        self.db_cursor = self.db_conn.cursor()
        self.login()

    def login(self):
        win = tk.Toplevel(self.root)
        win.title("Login")
        
        lab_username = tk.Label(win, text="Username: ")
        lab_username.pack()
        username = tk.Entry(win)
        username.pack()

        lab_pass = tk.Label(win, text="Password: ")
        password = tk.Entry(win, show="*")
        password.pack()

        win.mainloop()