from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"

class CompensationInterval(str, Enum):
    YEARLY = "yearly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"
    HOURLY = "hourly"

class Compensation(BaseModel):
    interval: Optional[CompensationInterval] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: Optional[str] = "ETB"

class JobPost(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    job_url: str
    description: Optional[str] = None
    date_posted: Optional[datetime] = None
    job_type: Optional[JobType] = None
    compensation: Optional[Compensation] = None
    site: str