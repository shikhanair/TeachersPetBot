import sqlite3

conn = sqlite3.connect("db.sqlite")

c = conn.cursor()

SQL_STATEMENT = """CREATE TABLE ta_office_hours (
    guild_id    INT,
    ta          VARCHAR(50),
    day         INT,
    begin_hr    INT,
    begin_min   INT,
    end_hr      INT,
    end_min     INT
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """CREATE TABLE exams (
    guild_id    INT,
    title       VARCHAR(50),
    desc        VARCHAR(300),
    date        VARCHAR(8),
    begin_hr    INT,
    begin_min   INT,
    end_hr      INT,
    end_min     INT
);"""

c.execute(SQL_STATEMENT)


SQL_STATEMENT = """CREATE TABLE assignments (
    guild_id    INT,
    title       VARCHAR(50),
    link        VARCHAR(300),
    desc        VARCHAR(300),
    date        VARCHAR(8),
    due_hr      INT,
    due_min     INT
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "test1",
    "test.html",
    "test desc",
    "09/25/2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "test2",
    "test2.html",
    "test2 desc",
    "09/26/2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "test1",
    "test desc",
    "09/27/2021",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "test2",
    "test2 desc",
    "09/28/2021",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO ta_office_hours VALUES(
    1,
    "john",
    "WED",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO ta_office_hours VALUES(
    1,
    "wendy",
    "THUR",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

conn.commit()

conn.close()