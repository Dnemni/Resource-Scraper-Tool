from pydantic import BaseModel, Field, ConfigDict
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

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Python Tutorial",
                    "url": "https://example.com/tutorial",
                    "description": "A comprehensive Python tutorial",
                    "resource_type": "course",
                    "credibility_score": 0.9,
                    "relevance_score": 0.95
                }
            ]
        }
    )

class SearchRequest(BaseModel):
    topic: str = Field(description="Topic to search for")
    resource_types: Optional[List[ResourceType]] = Field(
        default=None, description="List of resource types to filter by"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "topic": "Python programming",
                    "resource_types": ["video", "course"]
                }
            ]
        }
    )

class SearchResponse(BaseModel):
    resources: List[Resource] = Field(description="List of found resources")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "resources": [
                        {
                            "title": "Python Tutorial",
                            "url": "https://example.com/tutorial",
                            "description": "A comprehensive Python tutorial",
                            "resource_type": "course",
                            "credibility_score": 0.9,
                            "relevance_score": 0.95
                        }
                    ]
                }
            ]
        }
    )
