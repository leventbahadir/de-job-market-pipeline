CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.job_postings (
    id                  BIGSERIAL PRIMARY KEY,
    job_id              VARCHAR(255) UNIQUE NOT NULL,
    title               TEXT,
    company             TEXT,
    city                TEXT,
    is_remote           BOOLEAN,
    salary_min          NUMERIC,
    salary_max          NUMERIC,
    salary_avg          NUMERIC,
    contract_type       VARCHAR(100),
    description_clean   TEXT,
    ingested_at         TIMESTAMP,
    processed_at        TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staging.job_skills (
    id          BIGSERIAL PRIMARY KEY,
    job_id      VARCHAR(255),
    skill       VARCHAR(100),
    created_at  TIMESTAMP DEFAULT NOW()
);