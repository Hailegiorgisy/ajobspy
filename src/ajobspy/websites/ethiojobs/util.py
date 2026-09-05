import re
from datetime import datetime, timedelta

def clean_text(text: str) -> str:
    """Removes extra whitespace and newlines from scraped snippets."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def parse_relative_date(date_str: str) -> datetime | None:
    """Parses text strings like '2 hours ago' or 'September 14th, 2026' into a standard datetime object."""
    if not date_str:
        return None
    
    date_str = date_str.lower().strip()
    now = datetime.now()

    if "hour" in date_str or "minute" in date_str or "just now" in date_str:
        return now
    elif "day" in date_str:
        match = re.search(r'(\d+)', date_str)
        if match:
            days = int(match.group(1))
            return now - timedelta(days=days)
    
    # Fallback to standard formats
    for fmt in ("%B %dth, %Y", "%B %dst, %Y", "%B %dnd, %Y", "%B %drd, %Y", "%Y-%m-%d"):
        try:
            # Clean ordinal suffixes if present
            cleaned_date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
            return datetime.strptime(cleaned_date, fmt)
        except ValueError:
            continue
            
    return None