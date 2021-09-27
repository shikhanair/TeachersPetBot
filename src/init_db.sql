CREATE TABLE ta_office_hours (
    guild_id    INT,
    ta          VARCHAR(50),
    day         INT,
    begin_hr    INT,
    begin_min   INT,
    end_hr      INT,
    end_min     INT
);

CREATE TABLE exams (
    guild_id    INT,
    title       VARCHAR(50),
    desc        VARCHAR(300),
    date        VARCHAR(10),
    begin_hr    INT,
    begin_min   INT,
    end_hr      INT,
    end_min     INT
);

CREATE TABLE assignments (
    guild_id    INT,
    title       VARCHAR(50),
    link        VARCHAR(300),
    desc        VARCHAR(300),
    date        VARCHAR(10),
    due_hr      INT,
    due_min     INT
);