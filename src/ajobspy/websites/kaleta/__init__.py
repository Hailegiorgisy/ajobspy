import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from datetime import datetime
from ...model import JobPost, JobType, Compensation
from .constant import BASE_URL, SEARCH_URL, HEADERS
from .util import clean_text

def scrape_kaleta(
    search_term: Optional[str] = None,
    location: Optional[str] = "Central Africa",
    results_wanted: int = 20
) -> pd.DataFrame:
    """
    Scrapes pan-African and Central/East African listings from Kaleta.co job directory.
    """
    job_list = []
    params = {}
    if search_term:
        params["keywords"] = search_term

    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Kaleta structure uses list cards / table items
            job_cards = soup.select("div.job-item, div.card, article, div.content-box, li.job-post")
            if not job_cards:
                job_cards = soup.select("div[class*='job'], div[class*='listing']")

            for card in job_cards:
                if len(job_list) >= results_wanted:
                    break

                title_elem = card.select_one("h3 a, h4 a, a.job-title, a[href*='job']")
                if not title_elem:
                    continue

                title = clean_text(title_elem.text)
                company_elem = card.select_one(".company-name, span.employer, div.company, span[class*='company']")
                company = clean_text(company_elem.text) if company_elem else "International / NGO"

                location_elem = card.select_one(".location, span.region, div.job-location, span[class*='location']")
                loc = clean_text(location_elem.text) if location_elem else location

                job_url = title_elem.get('href', '')
                if job_url and not job_url.startswith("http"):
                    job_url = BASE_URL + job_url.lstrip('/')

                job_post = JobPost(
                    title=title,
                    company=company,
                    location=loc,
                    job_url=job_url,
                    date_posted=datetime.now(),
                    site="kaleta_regional",
                    job_type=JobType.FULL_TIME
                )
                job_list.append(job_post)
    except Exception as e:
        print(f"Error scraping Kaleta: {e}")

    if not job_list:
        return pd.DataFrame(columns=["id", "title", "company", "location", "job_url", "description", "date_posted", "job_type", "compensation", "site"])

    data = [job.model_dump() for job in job_list[:results_wanted]]
    return pd.DataFrame(data)