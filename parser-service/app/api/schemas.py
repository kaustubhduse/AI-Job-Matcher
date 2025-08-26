from pydantic import BaseModel
from typing import List, Optional

class ParseResponse(BaseModel):
    """
    Defines the JSON response after a resume is successfully parsed.
    """
    resume_id: int
    file_name: str
    message: str
    content: str # The full parsed text of the resume

class Job(BaseModel):
    """
    Defines the structure of a single job listing.
    """
    id: int
    title: str
    company: str
    description: str
    match_score: float

class MatchResponse(BaseModel):
    """
    Defines the JSON response for a job match request.
    """
    resume_id: int
    matches: List[Job]