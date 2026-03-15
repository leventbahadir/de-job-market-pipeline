CREATE SCHEMA IF NOT EXISTS marts;

CREATE TABLE IF NOT EXISTS marts.skill_demand (
    skill           VARCHAR(100) PRIMARY KEY,
    job_count       INT,
    pct_of_total    NUMERIC(5,2),
    last_updated    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS marts.salary_by_skill (
    skill           VARCHAR(100) PRIMARY KEY,
    avg_salary_min  NUMERIC,
    avg_salary_max  NUMERIC,
    sample_size     INT,
    last_updated    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS marts.jobs_by_location (
    city            TEXT,
    is_remote       BOOLEAN,
    job_count       INT,
    last_updated    TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (city, is_remote)
);

CREATE TABLE IF NOT EXISTS marts.top_companies (
    company         TEXT PRIMARY KEY,
    job_count       INT,
    last_updated    TIMESTAMP DEFAULT NOW()
);