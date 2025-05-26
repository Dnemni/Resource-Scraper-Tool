FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y curl gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run FastAPI with Uvicorn
CMD ["uvicorn", "resource_scraper.api:app", "--host", "0.0.0.0", "--port", "8080"] 