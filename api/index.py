from resource_scraper.api import app
from mangum import Mangum

import pydantic
import fastapi

print("🚨 Pydantic version:", pydantic.__version__)
print("🚨 FastAPI version:", fastapi.__version__)


handler = Mangum(app) 