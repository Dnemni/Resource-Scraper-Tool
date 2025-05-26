from resource_scraper.api import app
from mangum import Mangum

# Create handler for Vercel
handler = Mangum(app) 