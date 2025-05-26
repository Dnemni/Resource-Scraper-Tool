FROM python:3.10-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential curl

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Start FastAPI using Uvicorn
CMD ["uvicorn", "resource_scraper.api:app", "--host", "0.0.0.0", "--port", "8080"] 