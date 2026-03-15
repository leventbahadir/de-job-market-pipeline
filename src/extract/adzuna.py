import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search"

def fetch_jobs(keywords="data engineer", pages=5):
    jobs = []
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 50,
            "what": keywords,
            "content-type": "application/json"
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            break
        data = response.json()
        results = data.get("results", [])
        jobs.extend(results)
        print(f"Page {page}: fetched {len(results)} jobs")
    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"Total jobs fetched: {len(jobs)}")
    if jobs:
        print("Sample job:", jobs[0].get("title"), "|", jobs[0].get("company", {}).get("display_name"))
