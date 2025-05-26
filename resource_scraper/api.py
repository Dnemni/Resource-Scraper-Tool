from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SearchRequest, SearchResponse, Resource
from .scraper import ResourceScraper

app = FastAPI(
    title="Educational Resource Scraper API",
    description="API for finding high-quality educational resources for any topic",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = ResourceScraper()

@app.post("/api/search", response_model=SearchResponse)
async def search_resources(request: SearchRequest):
    """
    Search for educational resources based on a topic.
    
    - **topic**: The subject or topic to search for
    - **resource_types**: Optional list of specific resource types to filter by
    """
    try:
        resources = await scraper.search_resources(request.topic)
        
        # Filter by resource type if specified
        if request.resource_types:
            resources = [r for r in resources if r.resource_type in request.resource_types]
            
        return SearchResponse(
            resources=resources,
            total_results=len(resources)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resource-types")
async def get_resource_types():
    """Get all available resource types"""
    from .models import ResourceType
    return {"resource_types": [{"value": t.value, "label": t.value.title()} for t in ResourceType]}

@app.get("/health")
async def health_check():
    """Check if the API is running"""
    return {"status": "healthy"} 