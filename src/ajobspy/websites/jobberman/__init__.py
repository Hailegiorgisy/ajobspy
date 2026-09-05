import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional
from ...model import JobPost, JobType, Compensation
from .constant import BASE_URL, SEARCH_URL, HEADERS
from .util import clean_text, parse_jobberman_date

def scrape_jobberman(
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    country_tld: str = "com",
    results_wanted: int = 20
) -> pd.DataFrame:
    """
    Scrapes job listings from Jobberman (Nigeria/Ghana) and returns a Pandas DataFrame.
    """
    base_url = f"https://www.jobberman.{country_tld}"
    search_url = f"{base_url}/jobs"
    
    job_list = []
    params = {}
    if search_term:
        params["q"] = search_term
    if location:
        params["location"] = location

    page = 1
    while len(job_list) < results_wanted:
        params["page"] = page
        try:
            response = requests.get(search_url, headers=HEADERS, params=params, timeout=15)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Jobberman uses structured card containers layout blocks for search results.
            job_cards = soup.select(".job-card, div.bg-white.rounded-lg, div[class*='listing']")
            if not job_cards:
                job_cards = soup.select("div.row div.p-5, article")

            if not job_cards:
                break

            found_on_page = 0
            for card in job_cards:
                if len(job_list) >= results_wanted:
                    break

                title_elem = card.select_one("a.text-lg, h3 a, a[href*='/listings/'], div.text-xl a")
                if not title_elem:
                    continue

                found_on_page += 1
                title = clean_text(title_elem.text)
                
                company_elem = card.select_one(".text-sm.text-gray-500, .company-name, a[href*='employer']")
                company = clean_text(company_elem.text) if company_elem else "N/A"

                location_elem = card.select_one(".job-location, span[class*='location'], .text-gray-500 span")
                loc = clean_text(location_elem.text) if location_elem else ("Nigeria" if country_tld == "com" else "Ghana")

                date_elem = card.select_one("time, .job-age, span.text-gray-400, span[class*='date']")
                date_posted = parse_jobberman_date(date_elem.text) if date_elem else None

                job_url = title_elem.get('href', '')
                if job_url and not job_url.startswith("http"):
                    job_url = base_url + job_url

                job_post = JobPost(
                    title=title,
                    company=company,
                    location=loc,
                    job_url=job_url,
                    date_posted=date_posted,
                    site=f"jobberman_{country_tld}",
                    job_type=JobType.FULL_TIME
                )
                job_list.append(job_post)

            if found_on_page == 0:
                break

            next_page = soup.select_one("a[rel='next'], .pagination .next, li.pagination-next a")
            if not next_page:
                next_page = soup.find("a", string=lambda text: text and "next" in text.lower())

            if not next_page:
                break
            page += 1

        except Exception as e:
            print(f"Error scraping Jobberman: {e}")
            break

    if not job_list:
        return pd.DataFrame(columns=["id", "title", "company", "location", "job_url", "description", "date_posted", "job_type", "compensation", "site"])

    data = [job.model_dump() for job in job_list[:results_wanted]]
    return pd.DataFrame(data)