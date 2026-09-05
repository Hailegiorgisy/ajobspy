import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from datetime import datetime
from ...model import JobPost, JobType

def scrape_wuzzuf(
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    results_wanted: int = 20
) -> pd.DataFrame:
    """
    Scrapes North Africa / Egypt listings via lightweight endpoints.
    """
    job_list = []
    term = search_term.replace(" ", "+") if search_term else "software"
    url = f"https://wuzzuf.net/search/jobs/?q={term}"

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for generic container classes used in Wuzzuf's markup layout
            cards = soup.find_all(class_=lambda x: x and ('css-1gatmva' in x or 'job-item' in x or 'card' in x))
            
            if not cards:
                # Fallback generic anchor search for job titles
                cards = soup.select("h2 a")

            for card in cards:
                if len(job_list) >= results_wanted:
                    break

                if card.name == 'a':
                    title_elem = card
                else:
                    title_elem = card.select_one("h2 a, a[class*='title']")

                if not title_elem:
                    continue

                title = title_elem.text.strip()
                job_url = title_elem.get('href', '')
                if job_url and not job_url.startswith("http"):
                    job_url = "https://wuzzuf.net" + job_url

                job_list.append(JobPost(
                    title=title,
                    company="North Africa Employer",
                    location="Egypt / Remote",
                    job_url=job_url,
                    date_posted=datetime.now(),
                    site="wuzzuf_north_africa",
                    job_type=JobType.FULL_TIME
                ))
    except Exception as e:
        print(f"Error scraping Wuzzuf: {e}")

    if not job_list:
        return pd.DataFrame(columns=["id", "title", "company", "location", "job_url", "description", "date_posted", "job_type", "compensation", "site"])

    df = pd.DataFrame([j.model_dump() for j in job_list])
    return df.drop_duplicates(subset=['job_url']).head(results_wanted)