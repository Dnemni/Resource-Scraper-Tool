from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ResourceType(str, Enum):
    VIDEO = "video"
    COURSE = "course"
    DOCUMENTATION = "documentation"
    PRACTICE = "practice"
    OTHER = "other"

class Resource(BaseModel):
    title: str
    url: str
    description: str
    resource_type: str
    credibility_score: float
    relevance_score: float
    
class SearchRequest(BaseModel):
    topic: str
    resource_types: Optional[List[ResourceType]] = None
    
class SearchResponse(BaseModel):
    resources: List[Resource] 