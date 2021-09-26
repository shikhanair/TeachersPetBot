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
    "assign1",
    "assign1.html",
    "assign1 desc",
    "09/25/2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "assign3",
    "assign3.html",
    "assign3 desc",
    "09/26/2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "assign2",
    "assign2.html",
    "assign2 desc",
    "09/26/2021",
    15,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "test2",
    "test2 desc",
    "09/27/2021",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "test3",
    "test3 desc",
    "09/28/2021",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "test1",
    "test1 desc",
    "09/26/2021",
    14,
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