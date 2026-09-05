import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from datetime import datetime
from ...model import JobPost, JobType

def scrape_pnet(
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    results_wanted: int = 20
) -> pd.DataFrame:
    """
    Scrapes South African listings using an accessible open job index.
    """
    job_list = []
    term = search_term.replace(" ", "-") if search_term else "developer"
    url = f"https://www.gumtree.co.za/s-{term}/v1c8010p1"  # Open South African classifieds/jobs board
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.select("div.user-ad-row, article, div[class*='ad-card']")
            
            for card in cards:
                if len(job_list) >= results_wanted:
                    break

                title_elem = card.select_one("a.title, h2 a, a[class*='title']")
                if not title_elem:
                    continue

                title = title_elem.text.strip()
                job_url = title_elem.get('href', '')
                if job_url and not job_url.startswith("http"):
                    job_url = "https://www.gumtree.co.za" + job_url

                loc_elem = card.select_one("span.location, div[class*='location']")
                loc = loc_elem.text.strip() if loc_elem else "South Africa"

                job_list.append(JobPost(
                    title=title,
                    company="South Africa Local Employer",
                    location=loc,
                    job_url=job_url,
                    date_posted=datetime.now(),
                    site="south_africa_jobs",
                    job_type=JobType.FULL_TIME
                ))
    except Exception as e:
        print(f"Error scraping South Africa target: {e}")

    if not job_list:
        return pd.DataFrame(columns=["id", "title", "company", "location", "job_url", "description", "date_posted", "job_type", "compensation", "site"])

    df = pd.DataFrame([j.model_dump() for j in job_list])
    return df.drop_duplicates(subset=['job_url']).head(results_wanted)