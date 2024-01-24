import tkinter as tk
from tkinter import ttk

from tkcalendar import Calendar
from datetime import date

import settings
import sqlite3

from passwords import checkPassword

class App:
    def __init__(self, root):
        self.root = root
        self.db_conn = sqlite3.connect(settings.DB_PATH)
        self.db_cursor = self.db_conn.cursor()
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

        self.db_cursor.execute(f"""
            SELECT id, username, password
            FROM auth_user
            WHERE username = '{u}'
        """)

        user = self.db_cursor.fetchone()

        if checkPassword(p, user[2]):
            self.user = user
            win.destroy()

            self.db_cursor.execute(f"""
                SELECT id, name, description, date, done
                FROM task_task
            """)

            sql_tasks = self.db_cursor.fetchall()
            self.tasks = []
            i=0
            for t in sql_tasks:
                self.tasks.append(Task(
                    id=t[0],
                    name=t[1],
                    desc=t[2],
                    date=t[3],
                    done=t[4],
                    frame=self.frame_tasks,
                    row=i,
                ))
                i+=1
        else:
            win.destroy()
            self.loginWin()

    def appLayout(self):
        frame_date = tk.Frame(self.root)
        frame_date.pack(side="left")

        # Time navigation
        calendar = self.cal = Calendar(frame_date)
        calendar.pack(side="top")
        btn_day_prev = self.btn_day_prev = tk.Button(frame_date, text="Previous")
        btn_day_prev.pack(side="left")
        lab_day = self.lab_day = tk.Label(frame_date, text="Today")
        lab_day.pack(side="left")
        btn_day_next = self.btn_day_next = tk.Button(frame_date, text="Next")
        btn_day_next.pack(side="left")
        btn_add_task = self.btn_add_task = tk.Button(frame_date, text="Add a new task", command=self.new_task)
        btn_add_task.pack()

        # Tasks frame
        frame_tasks = self.frame_tasks = tk.Frame(self.root)
        frame_tasks.pack(side="left")
        # foreach task
        # task = tk.Label(frame_tasks, text="This is a task", padx=10)
        # task.grid(column=0, row=0)
        # btn_done_task = tk.Button(frame_tasks, text="Done")
        # btn_done_task.grid(column=1, row=0)
        # btn_del_task = tk.Button(frame_tasks, text="Delete")
        # btn_del_task.grid(column=2, row=0)

    def new_task(self):
        win = tk.Toplevel(self.root)

        lab_new_name = self.lab_new_name = tk.Label(win, text="Name: ")
        lab_new_name.grid(column=0, row=0)
        new_name = self.new_name = tk.Entry(win)
        new_name.grid(column=1, row=0)
        lab_new_date = self.lab_new_date = tk.Label(win, text="Date: ")
        lab_new_date.grid(column=0, row=1)
        # new_date = self.new_date = Calendar(win)
        # new_date.grid(column=1, row=1)
        today = date.today()
        new_date = self.new_date = Calendar(
            win,
            selectmode = 'day',
            # year = today.year,
            # month = today.month,
            # day = today.day
        )
        new_date.grid(column=1, row=1)
        lab_new_desc = self.lab_new_desc = tk.Label(win, text="Description: ")
        lab_new_desc.grid(column=0, row=2)
        new_desc = self.new_desc = tk.Text(win, width=30, height=10)
        new_desc.grid(column=1, row=2)  

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

        self.db_cursor.execute(f"""
            INSERT INTO task_task (name, description, user_id, date, done)
            VALUES ('{name}', '{desc}', 1, '{date}', 0)
        """)
        self.db_conn.commit()

        win.destroy()

class Task:
    def __init__(self, id, name, desc, date, done, frame, row, render=True):
        self.id = id
        self.name = name
        self.description = desc
        self.date = date
        self.done = done
        self.frame = frame
        self.row = row
        if render: self.render()


    def render(self):
        self.label = tk.Label(self.frame, text=self.name, padx=10)
        self.btn_done = tk.Button(self.frame, text="Done")
        self.btn_del = tk.Button(self.frame, text="Delete")

        self.widgets = [self.label, self.btn_done, self.btn_del]
        i = 0
        for w in self.widgets:
            w.grid(column=i, row=self.row)
            i += 1
        

    def destroy(self):
        pass

    def done(self):
        pass

    def delete(self):
        pass