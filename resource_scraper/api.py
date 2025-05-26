from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SearchRequest, SearchResponse
from .scraper import ResourceScraper
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper
scraper = ResourceScraper()

@app.post("/api/search")
async def search_resources(request: SearchRequest):
    try:
        if not os.getenv("SERPER_API_KEY"):
            raise HTTPException(status_code=500, detail="API key not configured")

        resources = await scraper.search_resources(request.topic)
        
        if request.resource_types:
            resources = [r for r in resources if r.resource_type in request.resource_types]
            
        return {"resources": resources[:5]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resource-types")
async def get_resource_types():
    from .models import ResourceType
    return {"resource_types": [{"value": t.value, "label": t.value.title()} for t in ResourceType]}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 