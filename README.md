# ajobspy

A comprehensive multi-regional job scraping framework for African job boards and Telegram channels. Aggregate job listings from major employment websites and social platforms, normalize them into a unified data model, and export for analysis or distribution.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Multi-site scraping**: EthioJobs, Wuzzuf, Bayt, Jobberman, BrighterMonday, Kaleta, PNet, and more
- **Telegram integration**: Scrape job posts from public Telegram channels with regex-based text parsing
- **Unified data model**: All jobs normalized to a common `JobPost` schema with Pydantic validation
- **Async support**: Non-blocking scraping with Telethon for high-throughput Telegram extraction
- **Pandas export**: Built-in deduplication and DataFrame output for easy analysis

## Project Structure

```
ajobspy/
├── README.md                    # This file
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # pip-compatible dependencies
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── src/ajobspy/                 # Main package source
│   ├── __init__.py              # Package initialization
│   ├── model.py                 # Pydantic models: JobPost, JobType, Compensation
│   ├── exception.py             # Custom exceptions
│   ├── util.py                  # Shared utility functions
│   │
│   ├── telegram/                # Telegram channel scraper
│   │   ├── __init__.py          # Main async scraper using Telethon
│   │   ├── constant.py          # Default Telegram channels list
│   │   ├── client.py            # Telegram client setup (extensible)
│   │   ├── parser.py            # Text parsing utilities
│   │   └── channels_config.json # User-defined channel configuration
│   │
│   └── websites/                # Individual job board scrapers
│       ├── ethiojobs/           # EthioJobs.net scraper
│       │   ├── __init__.py      # Scraper logic (Next.js __NEXT_DATA__ extraction)
│       │   ├── constant.py      # Site URLs and headers
│       │   └── util.py          # Date parsing and text cleaning
│       ├── wuzzuf/              # Wuzzuf.net scraper
│       ├── bayt/                # Bayt.com scraper
│       ├── brightermonday/      # BrighterMonday scraper
│       ├── jobberman/           # Jobberman scraper
│       ├── kaleta/              # Kaleta scraper
│       └── pnet/                # PNet scraper
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_model.py            # Tests for data models
│   ├── test_websites.py         # Tests for website scrapers
│   ├── test_telegram.py         # Tests for Telegram scraper
│   └── conftest.py              # pytest fixtures and configuration
│
├── inspect_next_data.py         # Debug script for Next.js payload inspection
└── dist/                        # Built distributions (auto-generated)
```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip or poetry

### From Source

```bash
git clone https://github.com/Hailegiorgisy/ajobspy.git
cd ajobspy
pip install -e .
```

### With Optional Test Dependencies

```bash
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install ajobspy
```

## Quick Start

### Scrape EthioJobs

```python
from ajobspy.websites.ethiojobs import scrape_ethiojobs

# Basic search
df = scrape_ethiojobs(search_term="Python Developer", results_wanted=20)
print(df[['title', 'company', 'location', 'job_url']])

# Filter by location
df = scrape_ethiojobs(
    search_term="Data Analyst",
    location="Addis Ababa",
    results_wanted=30
)
```

### Scrape Telegram Channels

```python
import asyncio
from ajobspy.telegram import scrape_telegram_channel

async def main():
    df = await scrape_telegram_channel(
        channel_username="@ethio_jobs",
        api_id=YOUR_API_ID,  # Get from https://my.telegram.org/apps
        api_hash="YOUR_API_HASH",
        results_wanted=50,
        search_keyword="Django"  # Optional: filter by keyword
    )
    print(df[['title', 'company', 'location']])

asyncio.run(main())
```

### Export Results

```python
from ajobspy.websites.ethiojobs import scrape_ethiojobs

df = scrape_ethiojobs(search_term="Engineer", results_wanted=50)

# Export to CSV
df.to_csv("jobs.csv", index=False)

# Export to JSON
df.to_json("jobs.json", orient="records", indent=2)

# Export to Excel
df.to_excel("jobs.xlsx", index=False)
```

## Data Models

### JobPost

The core data structure for all scraped jobs:

```python
from ajobspy.model import JobPost, JobType, Compensation

job = JobPost(
    id="ethio_123",
    title="Senior Python Developer",
    company="TechCorp Ethiopia",
    location="Addis Ababa",
    job_url="https://ethiojobs.net/job/senior-python-dev",
    description="We are seeking a talented Python developer...",
    date_posted=datetime(2026, 9, 14),
    job_type=JobType.FULL_TIME,
    compensation=Compensation(
        min_amount=50000,
        max_amount=80000,
        currency="ETB",
        interval="yearly"
    ),
    site="ethiojobs"
)
```

### JobType Enum

```python
class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"
```

### Compensation

```python
class Compensation(BaseModel):
    interval: Optional[CompensationInterval] = None  # yearly, monthly, weekly, daily, hourly
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: Optional[str] = "ETB"
```

## Configuration

### Telegram Channels

Edit `src/ajobspy/telegram/channels_config.json` to customize default channels:

```json
{
  "channels": [
    {
      "username": "@ethio_jobs",
      "keywords": ["job", "vacancy", "position"],
      "enabled": true
    },
    {
      "username": "@freelance_ethio",
      "keywords": ["freelance", "remote"],
      "enabled": true
    }
  ]
}
```

### Environment Variables

Create a `.env` file for Telegram credentials:

```bash
TELEGRAM_API_ID=YOUR_API_ID
TELEGRAM_API_HASH=YOUR_API_HASH
```

Load in your script:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
```

## API Reference

### Website Scrapers

All website scrapers follow the same interface:

```python
def scrape_<site>(
    search_term: Optional[str] = None,
    location: Optional[str] = None,
    results_wanted: int = 20
) -> pd.DataFrame:
    """Scrapes jobs and returns deduplicated DataFrame."""
```

**Supported Sites:**
- `scrape_ethiojobs()` – EthioJobs.net
- `scrape_wuzzuf()` – Wuzzuf.net
- `scrape_bayt()` – Bayt.com
- `scrape_jobberman()` – Jobberman.com
- `scrape_brightermonday()` – BrighterMonday.com
- `scrape_kaleta()` – Kaleta.com
- `scrape_pnet()` – PNet.com

### Telegram Scraper

```python
async def scrape_telegram_channel(
    channel_username: str,
    api_id: int,
    api_hash: str,
    results_wanted: int = 50,
    search_keyword: Optional[str] = None
) -> pd.DataFrame:
    """Asynchronously scrapes job posts from a Telegram channel."""
```

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
# Test data models
pytest tests/test_model.py -v

# Test website scrapers
pytest tests/test_websites.py -v

# Test Telegram scraper
pytest tests/test_telegram.py -v

# Test with coverage
pytest tests/ --cov=src/ajobspy --cov-report=html
```

### Write New Tests

Tests use `pytest` and `unittest.mock` for mocking HTTP requests:

```python
import pytest
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_scrape_ethiojobs_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html>...</html>"
    
    from ajobspy.websites.ethiojobs import scrape_ethiojobs
    df = scrape_ethiojobs(search_term="Python", results_wanted=10)
    
    assert len(df) > 0
    assert 'title' in df.columns
```

## Performance Considerations

### Timeout Configuration

All HTTP requests use a 15-second timeout to prevent hanging on unresponsive servers:

```python
response = requests.get(url, headers=headers, timeout=15)
```

### Connection Pooling

The framework uses `requests` default connection pooling. For high-throughput scenarios, consider using `requests.Session()`:

```python
from requests import Session

session = Session()
response = session.get(url, timeout=15)
session.close()
```

### Async Telegram Scraping

Telegram scraping is fully async to handle concurrent channel operations. Example:

```python
import asyncio

async def scrape_multiple_channels():
    tasks = [
        scrape_telegram_channel("@ethio_jobs", api_id, api_hash, 50),
        scrape_telegram_channel("@freelance_ethio", api_id, api_hash, 50),
        scrape_telegram_channel("@effoyjobs", api_id, api_hash, 50),
    ]
    results = await asyncio.gather(*tasks)
    return pd.concat(results, ignore_index=True)

asyncio.run(scrape_multiple_channels())
```

### DataFrame Deduplication

All results are deduplicated by `job_url` before returning:

```python
df.drop_duplicates(subset=['job_url']).head(results_wanted)
```

## Troubleshooting

### Issue: "No __NEXT_DATA__ tag found" for EthioJobs

**Cause:** Website structure changed or the page uses client-side rendering.

**Solution:** Run the debug script to inspect the current page structure:

```bash
python inspect_next_data.py
```

### Issue: Telegram session file growing

**Cause:** Telethon stores session data in `africajobspy_session.session`.

**Solution:** Delete the session file to start fresh:

```bash
rm africajobspy_session.session
```

### Issue: Rate limiting on job boards

**Cause:** Too many requests in a short time.

**Solution:** Add delays between requests:

```python
import time
time.sleep(2)  # 2-second delay between requests
```

### Issue: Timeout errors

**Cause:** Slow network or unresponsive server.

**Solution:** Increase timeout or add retry logic:

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Development Setup

```bash
# Clone and install with dev dependencies
git clone https://github.com/Hailegiorgisy/ajobspy.git
cd ajobspy
pip install -e ".[dev]"

# Run linting and tests
black src/ajobspy
flake8 src/ajobspy
pytest tests/ -v
```

## Known Issues & Limitations

- **Website Scrapers**: Some scrapers (Wuzzuf, Bayt, Jobberman, etc.) are skeleton implementations and need full scraper logic.
- **Telegram Parsing**: Regex-based parsing works for structured posts but may struggle with heavily formatted or non-English text.
- **Rate Limiting**: Job boards may implement rate limiting; use delays between requests.
- **Session Persistence**: Telegram session files should be excluded from version control (already in `.gitignore`).

## License

MIT License – See [LICENSE](LICENSE) file for details.

## Author

**Hailegiorgis Yirgu**  
GitHub: [@Hailegiorgisy](https://github.com/Hailegiorgisy)

## Acknowledgments

- [Telethon](https://github.com/LonamiWebs/Telethon) – Telegram client library
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) – HTML parsing
- [Pydantic](https://docs.pydantic.dev/) – Data validation
- [Pandas](https://pandas.pydata.org/) – Data manipulation

## Support

For issues, questions, or suggestions:

1. Check [existing issues](https://github.com/Hailegiorgisy/ajobspy/issues)
2. [Open a new issue](https://github.com/Hailegiorgisy/ajobspy/issues/new)
3. Email: (maintainer contact info)

---

**Last Updated:** September 14, 2026
