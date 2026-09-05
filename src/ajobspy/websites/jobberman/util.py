import re
from datetime import datetime, timedelta

def clean_text(text: str) -> str:
    """Removes extra whitespace and newlines."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def parse_jobberman_date(date_str: str) -> datetime | None:
    """Parses relative timestamps like 'Today', '2 days ago', '1 week ago'."""
    if not date_str:
        return None
    
    date_str = date_str.lower().strip()
    now = datetime.now()

    if "today" in date_str or "just now" in date_str or "hour" in date_str:
        return now
    elif "yesterday" in date_str:
        return now - timedelta(days=1)
    
    match = re.search(r'(\d+)\s*(day|week|month|year)', date_str)
    if match:
        val = int(match.group(1))
        unit = match.group(2)
        if "day" in unit:
            return now - timedelta(days=val)
        elif "week" in unit:
            return now - timedelta(weeks=val)
        elif "month" in unit:
            return now - timedelta(days=val * 30)

    return None