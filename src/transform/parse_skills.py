import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

SKILLS = [
    "python", "sql", "spark", "kafka", "airflow", "dbt", "docker",
    "kubernetes", "aws", "gcp", "azure", "redshift", "snowflake",
    "bigquery", "postgres", "postgresql", "mysql", "mongodb",
    "pandas", "numpy", "scala", "java", "terraform", "glue",
    "athena", "s3", "etl", "elt", "pipeline", "databricks",
    "power bi", "tableau", "looker", "git", "linux"
]

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def parse_skills():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT job_id, title, description FROM raw.job_postings")
    jobs = cur.fetchall()

    skill_rows = []
    for job_id, title, description in jobs:
        text = f"{title or ''} {description or ''}".lower()
        for skill in SKILLS:
            if skill in text:
                skill_rows.append((job_id, skill))

    cur.execute("TRUNCATE TABLE staging.job_skills")
    cur.executemany("""
        INSERT INTO staging.job_skills (job_id, skill)
        VALUES (%s, %s)
    """, skill_rows)

    conn.commit()
    print(f"Parsed {len(jobs)} jobs, extracted {len(skill_rows)} skill mentions")

    cur.execute("""
        INSERT INTO marts.skill_demand (skill, job_count, pct_of_total, last_updated)
        SELECT
            skill,
            COUNT(*) as job_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT job_id) FROM staging.job_skills), 2) as pct_of_total,
            NOW()
        FROM staging.job_skills
        GROUP BY skill
        ORDER BY job_count DESC
        ON CONFLICT (skill) DO UPDATE
            SET job_count = EXCLUDED.job_count,
                pct_of_total = EXCLUDED.pct_of_total,
                last_updated = EXCLUDED.last_updated
    """)

    conn.commit()
    print("Marts updated.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    parse_skills()