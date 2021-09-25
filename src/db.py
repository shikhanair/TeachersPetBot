import sqlite3
from sqlite3 import Error
import os

con = None
def connect():
    global con
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite')
    try:
        con = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred when trying to connect to SQLite database")


def select_query(sql, args=()):
    cur = con.cursor()
    return cur.execute(sql, args)


def mutation_query(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    con.commit()
