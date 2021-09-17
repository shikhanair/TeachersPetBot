import psycopg2

def connect():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="",
            user="username",
            password="password"
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()