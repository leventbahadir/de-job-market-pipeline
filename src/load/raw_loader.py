import os
import psycopg2
from dotenv import load_dotenv
from src.extract.adzuna import fetch_jobs

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def load_raw(jobs):
    conn = get_connection()
    cur = conn.cursor()
    inserted = 0
    skipped = 0

    for job in jobs:
        try:
            cur.execute("""
                INSERT INTO raw.job_postings (
                    job_id, title, company, location, description,
                    salary_min, salary_max, contract_type, category,
                    redirect_url, created
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_id) DO NOTHING
            """, (
                job.get("id"),
                job.get("title"),
                job.get("company", {}).get("display_name"),
                job.get("location", {}).get("display_name"),
                job.get("description"),
                job.get("salary_min"),
                job.get("salary_max"),
                job.get("contract_type"),
                job.get("category", {}).get("label"),
                job.get("redirect_url"),
                job.get("created")
            ))
            inserted += 1
        except Exception as e:
            skipped += 1
            print(f"Skipped job: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted: {inserted} | Skipped (duplicates): {skipped}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    load_raw(jobs)