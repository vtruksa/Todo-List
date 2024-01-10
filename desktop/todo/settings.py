import os

CURR_PATH = os.getcwd()
print("Current: " + str(CURR_PATH))
#DB_PATH = os.path.abspath(os.path.join(CURR_PATH, '..', '..', '..', 'web/todo/db.sqlite3'))
DB_PATH = os.path.join(CURR_PATH, "web/todo/db.sqlite3")