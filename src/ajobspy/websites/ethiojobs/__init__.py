import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from typing import Optional
from ...model import JobPost, JobType, Compensation
from .constant import BASE_URL, SEARCH_URL, HEADERS
from .util import clean_text, parse_relative_date

def scrape_ethiojobs(
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    results_wanted: int = 20
) -> pd.DataFrame:
    """
    Scrapes job postings from EthioJobs.net via its Next.js __NEXT_DATA__ payload.
    """
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
            response = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=15)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            next_data_script = soup.select_one("script#__NEXT_DATA__")
            if not next_data_script or not next_data_script.string:
                break

            data = json.loads(next_data_script.string)
            page_props = data.get("props", {}).get("pageProps", {})
            
            # Extract jobs array from Next.js pageProps
            jobs_data = page_props.get("jobs", [])
            if isinstance(jobs_data, dict):
                jobs_data = jobs_data.get("data", [])
            
            if not jobs_data:
                break

            found_on_page = 0
            for item in jobs_data:
                if len(job_list) >= results_wanted:
                    break
                
                found_on_page += 1
                title = item.get("title") or item.get("job_title") or "N/A"
                
                # Handle company name structure (could be string or dict)
                company_raw = item.get("company") or item.get("company_name")
                if isinstance(company_raw, dict):
                    company = company_raw.get("name") or company_raw.get("title") or "N/A"
                else:
                    company = str(company_raw) if company_raw else "N/A"

                loc = item.get("location") or item.get("city") or "Ethiopia"
                
                # Construct clean job URL
                slug = item.get("slug") or item.get("id") or ""
                if slug and not str(slug).startswith("http"):
                    job_url = f"{BASE_URL}/job/{slug}"
                else:
                    job_url = item.get("url") or BASE_URL

                date_str = item.get("created_at") or item.get("posted_date") or item.get("date")
                date_posted = parse_relative_date(date_str) if date_str else None

                job_post = JobPost(
                    title=title,
                    company=company,
                    location=loc,
                    job_url=job_url,
                    date_posted=date_posted,
                    site="ethiojobs",
                    job_type=JobType.FULL_TIME
                )
                job_list.append(job_post)

            if found_on_page == 0:
                break
            
            page += 1

        except Exception as e:
            print(f"Error scraping EthioJobs via Next.js payload: {e}")
            break

    if not job_list:
        return pd.DataFrame(columns=["id", "title", "company", "location", "job_url", "description", "date_posted", "job_type", "compensation", "site"])

    data_rows = [job.model_dump() for job in job_list[:results_wanted]]
    return pd.DataFrame(data_rows)