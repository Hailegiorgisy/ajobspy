import re
from datetime import datetime, timedelta

def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def parse_kaleta_date(date_str: str) -> datetime | None:
    if not date_str:
        return None
    now = datetime.now()
    if "new" in date_str.lower():
        return now
    return now