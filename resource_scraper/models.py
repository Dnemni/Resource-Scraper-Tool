from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ResourceType(str, Enum):
    VIDEO = "video"
    COURSE = "course"
    DOCUMENTATION = "documentation"
    PRACTICE = "practice"
    OTHER = "other"

class Resource(BaseModel):
    title: str = Field(description="Title of the resource")
    url: str = Field(description="URL of the resource")
    description: str = Field(description="Description of the resource")
    resource_type: str = Field(description="Type of the resource")
    credibility_score: float = Field(description="Credibility score of the resource", ge=0.0, le=1.0)
    relevance_score: float = Field(description="Relevance score of the resource", ge=0.0, le=1.0)
    
class SearchRequest(BaseModel):
    topic: str = Field(description="Topic to search for")
    resource_types: Optional[List[ResourceType]] = Field(default=None, description="List of resource types to filter by")
    
class SearchResponse(BaseModel):
    resources: List[Resource] = Field(description="List of found resources") 