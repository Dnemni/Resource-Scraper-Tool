from fastapi import FastAPI
from resource_scraper.api import app

# Need to explicitly set root_path for Vercel deployment
app.root_path = ""

# Export for Vercel
app = app