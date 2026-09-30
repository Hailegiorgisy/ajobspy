import asyncio
from typing import List
from .models import JobListing, Location
from .adapters import ResilientRequestAdapter

class AsyncJobScraper:
    """High-performance non-blocking scraper engine."""
    def __init__(self, adapter: ResilientRequestAdapter = None):
        self.adapter = adapter or ResilientRequestAdapter()

    async def fetch_listings(self, query: str = "Data Scientist", mock_mode: bool = False) -> List[JobListing]:
        if mock_mode:
            await asyncio.sleep(0.05)  # simulate async delay
            return [
                JobListing(
                    id="mock-001",
                    title=f"Senior {query}",
                    company="HealthTech Africa",
                    location=Location(city="Addis Ababa", country="Ethiopia", is_remote=True),
                    skills_required=["Python", "FastAPI", "PostgreSQL", "Machine Learning"],
                    salary_range="$40,000 - $65,000",
                    source_url="https://example.com/jobs/mock-001",
                    description_snippet="Lead epidemiological machine learning modeling and pipeline development."
                ),
                JobListing(
                    id="mock-002",
                    title="Full Stack Software Engineer",
                    company="Global Health Informatics",
                    location=Location(city="Nairobi", country="Kenya", is_remote=True),
                    skills_required=["TypeScript", "React", "Node.js", "Docker"],
                    salary_range="$50,000 - $75,000",
                    source_url="https://example.com/jobs/mock-002",
                    description_snippet="Design and scale patient management portals and clinical registry interfaces."
                )
            ]
        
        # Real implementation hooks to live aggregator APIs
        raise NotImplementedError("Live endpoints require active proxy credentials. Use mock_mode=True for testing.")
