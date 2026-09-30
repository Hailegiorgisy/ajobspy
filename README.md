# ajobspy: Asynchronous Python Toolkit for Job Market Extraction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

An asynchronous, type-safe Python toolkit for extracting and standardizing job opportunities across global and regional job boards.

## Features
- **AsyncIO & HTTPX**: Non-blocking concurrency for high throughput.
- **Resilient Request Adapter**: Automatic retry logic with exponential backoff and proxy pool rotation.
- **Type Annotations**: Strict PEP 484 compliance using Pydantic models.
- **Mock Testing Layer**: Comprehensive test coverage without external network dependencies.

## Quickstart
```python
import asyncio
from ajobspy import AsyncJobScraper

async def main():
    scraper = AsyncJobScraper()
    listings = await scraper.fetch_listings(query="Clinical Data Scientist", mock_mode=True)
    for job in listings:
        print(f"[{job.company}] {job.title} - {job.salary_range}")

if __name__ == "__main__":
    asyncio.run(main())
```
