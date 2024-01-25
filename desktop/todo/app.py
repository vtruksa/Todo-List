import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar
from datetime import date

import settings
import sqlite3

from passwords import checkPassword

class App:
    global db_conn, db_cursor

    def __init__(self, root):
        global db_conn, db_cursor
        self.root = root
        db_conn = sqlite3.connect(settings.DB_PATH)
        db_cursor = db_conn.cursor()
        self.appLayout()
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

        db_cursor.execute(f"""
            SELECT id, username, password
            FROM auth_user
            WHERE username = '{u}'
        """)

        user = db_cursor.fetchone()

        if checkPassword(p, user[2]):
            self.user = user
            win.destroy()

            db_cursor.execute(f"""
                SELECT id, name, description, date, done
                FROM task_task
            """)

            sql_tasks = db_cursor.fetchall()
            self.tasks = []
            self.tasks_show = []
            
            for t in sql_tasks:
                self.tasks.append(Task(
                    id=t[0],
                    name=t[1],
                    desc=t[2],
                    date=t[3],
                    done=t[4],
                    frame=self.frame_tasks,
                ))
                if t[3] == str(date.today()): self.tasks_show.append(self.tasks[-1])

            if len(self.tasks_show) > 0:
                for i in range(0, len(self.tasks_show)): self.tasks_show[i].render(row=i)
            else: pass # TODO Add a label informing the user about having no tasks for the selected day
        else:
            win.destroy()
            self.loginWin()

    def appLayout(self):
        frame_date = tk.Frame(self.root)
        frame_date.pack(side="left")

        # Time navigation
        self.cal = Calendar(frame_date, selectmode="day", date_pattern="yyyy-mm-dd")
        self.cal.pack(side="top")
        self.cal.bind("<<CalendarSelected>>", self.date_change)

        self.add_task_btn = tk.Button(frame_date, text="Add a new task", command=self.new_task)
        self.add_task_btn.pack()

        # Tasks frame
        self.frame_tasks = tk.Frame(self.root)
        self.frame_tasks.pack(side="left")

    def date_change(self, event):
        date = self.cal.get_date()
        for t in self.tasks_show: t.destroy()
        self.tasks_show = []

        i = 0
        for t in self.tasks:
            if t.date == date: 
                self.tasks_show.append(t)
                t.render(i)
                i += 1

    def new_task(self):
        win = tk.Toplevel(self.root)

        self.lab_new_name = tk.Label(win, text="Name: ")
        self.lab_new_name.grid(column=0, row=0)
        self.new_name = tk.Entry(win)
        self.new_name.grid(column=1, row=0)
        self.lab_new_date = tk.Label(win, text="Date: ")
        self.lab_new_date.grid(column=0, row=1)
        today = date.today()
        self.new_date = Calendar(win, selectmode = 'day')
        self.new_date.grid(column=1, row=1)
        self.lab_new_desc = tk.Label(win, text="Description: ")
        self.lab_new_desc.grid(column=0, row=2)
        self.new_desc = tk.Text(win, width=30, height=10)
        self.new_desc.grid(column=1, row=2)  

        btn_add = tk.Button(win, text="Add", command=lambda: self.add_task(win))
        btn_add.grid(columnspan=2, row=3)

        win.mainloop()

    def add_task(self, win):
        name = self.new_name.get()
        date = self.new_date.get_date().split('/')
        # Format the date
        if len(date[0]) == 1: date[0] = "0" + date[0]
        date = str(int(date[2])+2000) + "-" + date[0] + "-" + date[1]

        desc = self.new_desc.get("1.0","end-1c")

        db_cursor.execute(f"""
            INSERT INTO task_task (name, description, user_id, date, done)
            VALUES ('{name}', '{desc}', 1, '{date}', 0)
        """)
        db_conn.commit()

        win.destroy()

class Task:
    def __init__(self, id, name, desc, date, done, frame):
        self.id = id
        self.name = name
        self.description = desc
        self.date = date
        self.done = done
        self.frame = frame
        self.widgets = []

    def render(self, row=0):
        if self.done == 0:
            self.label = tk.Label(self.frame, text=self.name, padx=10)
            self.btn_done = tk.Button(self.frame, text="Done", command=self.make_done)
            self.btn_del = tk.Button(self.frame, text="Delete", command=self.delete)

            self.widgets = [self.label, self.btn_done, self.btn_del]
        else:
            self.label = tk.Label(self.frame, text=self.name, padx=10, state="disabled")
            self.widgets = [self.label]
        
        i = 0
        for w in self.widgets:
            w.grid(column=i, row=row)
            i += 1
        

    def destroy(self): 
        for w in self.widgets: w.destroy()

    def make_done(self):
        global db_cursor
        self.done = 1
        db_cursor.execute(f"""
            UPDATE task_task
            SET done=1
            WHERE id={self.id}
        """)
        self.destroy()
        self.render()

    def delete(self):
        global db_cursor, db_conn
        db_cursor.execute(f"""
            DELETE FROM task_task
            WHERE id={self.id}
        """)
        db_conn.commit()
        self.destroy()
        del self