import fastapi
import pydantic
print("✅ Pydantic version:", pydantic.__version__)
print("✅ FastAPI version:", fastapi.__version__)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from resource_scraper.models import SearchRequest, SearchResponse, ResourceType
from resource_scraper.scraper import ResourceScraper
import os
from typing import List, Dict

app = FastAPI(
    title="Resource Scraper API",
    description="API for finding educational resources",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = ResourceScraper()

@app.post("/search", response_model=SearchResponse)
async def search_resources(request: SearchRequest) -> SearchResponse:
    """
    Search for educational resources based on topic and resource types.
    """
    try:
        if not os.getenv("SERPER_API_KEY"):
            raise HTTPException(status_code=500, detail="API key not configured")

        resources = await scraper.search_resources(request.topic)
        
        if request.resource_types:
            resources = [r for r in resources if ResourceType(r.resource_type) in request.resource_types]
            
        return SearchResponse(resources=resources[:5])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resource-types")
async def get_resource_types() -> Dict[str, List[Dict[str, str]]]:
    """
    Get available resource types.
    """
    return {
        "resource_types": [
            {"value": t.value, "label": t.value.title()} 
            for t in ResourceType
        ]
    }

@app.get("/")
async def health_check() -> Dict[str, str]:
    """
    Check API health.
    """
    return {"status": "healthy"} 