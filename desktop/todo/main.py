import tkinter as tk
from tkinter import ttk

from app import App

root = tk.Tk()
root.title("TODO List")

s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()

root.geometry(f"{int(s_w/4)}x{int(s_h/2)}+{int(s_w/4)}+{int(s_h/4)}")
root.resizable(False, False)

App(root)
root.mainloop()