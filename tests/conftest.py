"""Pytest configuration and fixtures for ajobspy tests."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock
from ajobspy.model import JobPost, JobType, Compensation, CompensationInterval


@pytest.fixture
def sample_job_post():
    """Create a sample JobPost for testing."""
    return JobPost(
        id="test_123",
        title="Senior Python Developer",
        company="TechCorp Ethiopia",
        location="Addis Ababa",
        job_url="https://ethiojobs.net/job/senior-python-dev",
        description="We are seeking a talented Python developer with 5+ years experience.",
        date_posted=datetime(2026, 9, 14),
        job_type=JobType.FULL_TIME,
        compensation=Compensation(
            min_amount=50000,
            max_amount=80000,
            currency="ETB",
            interval=CompensationInterval.YEARLY
        ),
        site="ethiojobs"
    )


@pytest.fixture
def sample_jobs_list():
    """Create a list of sample JobPosts for testing."""
    return [
        JobPost(
            id="test_001",
            title="Python Developer",
            company="Company A",
            location="Addis Ababa",
            job_url="https://example.com/job/001",
            description="Python development role",
            date_posted=datetime(2026, 9, 14),
            job_type=JobType.FULL_TIME,
            site="test_site"
        ),
        JobPost(
            id="test_002",
            title="Data Analyst",
            company="Company B",
            location="Nairobi",
            job_url="https://example.com/job/002",
            description="Data analysis role",
            date_posted=datetime(2026, 9, 13),
            job_type=JobType.FULL_TIME,
            site="test_site"
        ),
        JobPost(
            id="test_003",
            title="DevOps Engineer",
            company="Company C",
            location="Lagos",
            job_url="https://example.com/job/003",
            description="DevOps engineering role",
            date_posted=datetime(2026, 9, 12),
            job_type=JobType.CONTRACT,
            compensation=Compensation(
                min_amount=100000,
                max_amount=150000,
                currency="USD",
                interval=CompensationInterval.YEARLY
            ),
            site="test_site"
        ),
    ]


@pytest.fixture
def mock_requests_get(monkeypatch):
    """Mock requests.get for testing."""
    mock = MagicMock()
    monkeypatch.setattr("requests.get", mock)
    return mock


@pytest.fixture
def sample_html_response():
    """Sample HTML response from a job board."""
    return """
    <html>
        <head><title>Jobs</title></head>
        <body>
            <div class="job-listing">
                <h2 class="job-title">Python Developer</h2>
                <p class="company">TechCorp</p>
                <p class="location">Addis Ababa</p>
                <p class="date">2 days ago</p>
            </div>
            <div class="job-listing">
                <h2 class="job-title">Data Analyst</h2>
                <p class="company">DataCorp</p>
                <p class="location">Nairobi</p>
                <p class="date">1 day ago</p>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def sample_telegram_messages():
    """Sample Telegram messages containing job posts."""
    return [
        {
            "id": 100,
            "message": "🔥 HIRING: Senior Python Developer\n"
                      "Company: TechCorp\n"
                      "Location: Addis Ababa\n"
                      "Salary: 50K - 80K ETB\n"
                      "Type: Full-time\n"
                      "Apply: https://example.com/apply/100",
            "date": datetime(2026, 9, 14, 10, 30),
        },
        {
            "id": 101,
            "message": "📢 JOB ALERT: Data Analyst\n"
                      "Company: DataCorp\n"
                      "Location: Nairobi\n"
                      "Apply: https://example.com/apply/101",
            "date": datetime(2026, 9, 14, 11, 0),
        },
        {
            "id": 102,
            "message": "🚀 Freelance opportunity: Web Developer (React)\n"
                      "Budget: $50-100/hour\n"
                      "Contact: @freelancer_xyz",
            "date": datetime(2026, 9, 14, 11, 30),
        },
    ]


@pytest.fixture
def sample_next_data_json():
    """Sample __NEXT_DATA__ JSON from EthioJobs."""
    return {
        "props": {
            "pageProps": {
                "jobs": [
                    {
                        "id": "job_1",
                        "title": "Senior Software Engineer",
                        "company": {"name": "TechCorp"},
                        "location": "Addis Ababa",
                        "salary": {"min": 50000, "max": 80000, "currency": "ETB"},
                        "jobType": "full_time",
                        "postedDate": "2026-09-14",
                        "description": "We are looking for...",
                        "url": "https://ethiojobs.net/job/senior-software-engineer"
                    },
                    {
                        "id": "job_2",
                        "title": "Junior Python Developer",
                        "company": {"name": "StartupXYZ"},
                        "location": "Nairobi",
                        "salary": None,
                        "jobType": "full_time",
                        "postedDate": "2026-09-13",
                        "description": "Python development...",
                        "url": "https://ethiojobs.net/job/junior-python-developer"
                    }
                ]
            }
        }
    }
