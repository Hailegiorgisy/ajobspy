import pytest
from ajobspy import AsyncJobScraper, JobListing

@pytest.mark.asyncio
async def test_async_scraper_mock():
    scraper = AsyncJobScraper()
    jobs = await scraper.fetch_listings(query="Data Scientist", mock_mode=True)
    assert len(jobs) == 2
    assert isinstance(jobs[0], JobListing)
    assert "Python" in jobs[0].skills_required
    assert jobs[0].location.is_remote is True
