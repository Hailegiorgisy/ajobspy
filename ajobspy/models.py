from typing import Optional, List
from pydantic import BaseModel, Field

class Location(BaseModel):
    city: Optional[str] = None
    country: str = "Ethiopia"
    is_remote: bool = False

class JobListing(BaseModel):
    id: str
    title: str
    company: str
    location: Location
    skills_required: List[str] = Field(default_factory=list)
    salary_range: Optional[str] = None
    source_url: str
    description_snippet: Optional[str] = None
