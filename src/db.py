import sqlite3
from sqlite3 import Error

con = None
def connect():
    global con
    try:
        con = sqlite3.connect('db.sqlite')
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred when trying to connect to SQLite database")


def select_query(sql):
    cur = con.cursor()
    return cur.execute(sql)


def mutation_query(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    con.commit()
