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
    date        VARCHAR(10),
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
    date        VARCHAR(10),
    due_hr      INT,
    due_min     INT
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "Assignment #1",
    "https://drive.google.com/assign1.html",
    "Covers lecture material up to to the due date.",
    "09-25-2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "Assignment #1.2",
    "https://drive.google.com/assign1.html",
    "Covers lecture material up to to the due date.",
    "09-26-2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO assignments VALUES(
    1,
    "Assignment #2",
    "https://drive.google.com/assign2.html",
    "Covers lecture material up to to the due date.",
    "09-28-2021",
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "Exam 1",
    "All materials up to the date of the exam.",
    "09-29-2021",
    10,
    30,
    11,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "Exam 2",
    "All materials up to the date of the exam, except material covered by previous exam.",
    "10-06-2021",
    16,
    30,
    18,
    30
);"""

c.execute(SQL_STATEMENT)

SQL_STATEMENT = """INSERT INTO exams VALUES(
    1,
    "Final Exam",
    "Final exam - covers everything taught!",
    "12-02-2021",
    14,
    30,
    18,
    30
);"""


c.execute(SQL_STATEMENT)

conn.commit()

conn.close()