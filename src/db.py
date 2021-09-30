import sqlite3
from sqlite3 import Error
import os

CON = None
def connect():
    ''' connect program to database file db.sqlite '''
    global CON
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite')
    try:
        CON = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred when trying to connect to SQLite database")


def select_query(sql, args=()):
    ''' select query to return items from database '''
    cur = CON.cursor()
    return cur.execute(sql, args)


def mutation_query(sql, args=()):
    ''' do a mutation on the database '''
    cur = CON.cursor()
    cur.execute(sql, args)
    CON.commit()
