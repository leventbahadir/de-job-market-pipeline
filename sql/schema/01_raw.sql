CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.job_postings (
    id                  BIGSERIAL PRIMARY KEY,
    job_id              VARCHAR(255) UNIQUE NOT NULL,
    title               TEXT,
    company             TEXT,
    location            TEXT,
    description         TEXT,
    salary_min          NUMERIC,
    salary_max          NUMERIC,
    contract_type       VARCHAR(100),
    category            TEXT,
    redirect_url        TEXT,
    created             TIMESTAMP,
    ingested_at         TIMESTAMP DEFAULT NOW()
);