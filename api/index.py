from resource_scraper.api import app

# For local dev
if __name__ == "__main__":
    import uvicorn
    import fastapi, pydantic
    print("✅ FastAPI version:", fastapi.__version__)
    print("✅ Pydantic version:", pydantic.__version__)
    uvicorn.run(app, host="0.0.0.0", port=8000)
