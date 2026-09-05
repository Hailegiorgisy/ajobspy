import os
import re
import pandas as pd
from typing import List, Optional
from datetime import datetime
from telethon import TelegramClient
from ajobspy.model import JobPost, JobType

def parse_telegram_post(text: str) -> dict:
    """
    Extracts key fields from unstructured Telegram job posts using regex heuristics.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Default fallback title is the first non-empty line
    title = lines[0][:100] if lines else "Untitled Position"
    company = "Telegram Channel Employer"
    location = "Ethiopia / Remote"
    
    full_text = " ".join(lines)
    
    # Look for common label patterns (e.g., "Position:", "Company:", "Location:")
    for line in lines:
        lower_line = line.lower()
        if any(k in lower_line for k in ["position", "job title", "role", "የሥራ መደብ"]):
            parts = re.split(r'[:|-]', line, 1)
            if len(parts) > 1 and len(parts[1].strip()) > 2:
                title = parts[1].strip()
        elif any(k in lower_line for k in ["company", "organization", "org", "ድርጅት"]):
            parts = re.split(r'[:|-]', line, 1)
            if len(parts) > 1 and len(parts[1].strip()) > 2:
                company = parts[1].strip()
        elif any(k in lower_line for k in ["location", "place", "workplace", "ቦታ"]):
            parts = re.split(r'[:|-]', line, 1)
            if len(parts) > 1 and len(parts[1].strip()) > 2:
                location = parts[1].strip()

    return {
        "title": clean_text(title),
        "company": clean_text(company),
        "location": clean_text(location)
    }

def clean_text(text: str) -> str:
    return re.sub(r'[\*\_#`]', '', text).strip()

async def scrape_telegram_channel(
    channel_username: str,
    api_id: int,
    api_hash: int,
    results_wanted: int = 50,
    search_keyword: Optional[str] = None
) -> pd.DataFrame:
    """
    Asynchronously scrapes job posts from a public Telegram channel using Telethon.
    """
    job_list = []
    client = TelegramClient('africajobspy_session', api_id, api_hash)
    
    async with client:
        try:
            entity = await client.get_entity(channel_username)
            async for message in client.iter_messages(entity, limit=results_wanted * 3):
                if len(job_list) >= results_wanted:
                    break
                
                if not message.text:
                    continue
                
                text = message.text.strip()
                
                # Exclude channel boilerplate ads/bots if necessary
                if "ETOJobsbot" in text or len(text) < 40:
                    continue
                
                if search_keyword and search_keyword.lower() not in text.lower():
                    continue
                
                parsed = parse_telegram_post(text)
                
                channel_name_clean = channel_username.replace("https://t.me/", "").replace("@", "")
                job_url = f"https://t.me/{channel_name_clean}/{message.id}"
                
                job_post = JobPost(
                    title=parsed["title"],
                    company=parsed["company"],
                    location=parsed["location"],
                    job_url=job_url,
                    description=text,
                    date_posted=message.date.replace(tzinfo=None) if message.date else datetime.now(),
                    site=f"telegram_{channel_name_clean}",
                    job_type=JobType.FULL_TIME
                )
                job_list.append(job_post)
                
        except Exception as e:
            print(f"Error reading Telegram channel {channel_username}: {e}")

    if not job_list:
        return pd.DataFrame(columns=["id", "title", "company", "location", "job_url", "description", "date_posted", "job_type", "compensation", "site"])

    df = pd.DataFrame([j.model_dump() for j in job_list])
    return df.drop_duplicates(subset=['job_url']).head(results_wanted)