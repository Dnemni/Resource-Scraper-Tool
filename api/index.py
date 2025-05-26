import fastapi
import pydantic
print("✅ FastAPI version:", fastapi.__version__)
print("✅ Pydantic version:", pydantic.__version__)

from resource_scraper.api import app
from mangum import Mangum

# Create handler for Vercel
handler = Mangum(app, lifespan="off")

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 