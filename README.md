# Educational Resource Scraper

A powerful tool that scrapes the web to find and recommend high-quality educational resources for any topic. The tool uses AI to analyze and rank resources based on credibility, relevance, and source quality.

## Features

- **Smart Resource Discovery**:
  - YouTube explainer videos
  - Khan Academy / MIT OCW lessons
  - Technical documentation and tutorials
  - Practice resources (LeetCode, Quizlet, etc.)
- **Intelligent Ranking**:
  - Source credibility scoring
  - Content relevance matching
  - Educational value assessment
- **Multiple Interfaces**:
  - RESTful API
  - Command-line interface
  - React component
- **Resource Types**:
  - Videos
  - Courses
  - Documentation
  - Practice platforms
  - Other educational resources

## Project Structure

```
resource-scraper/
├── resource_scraper/           # Main package directory
│   ├── __init__.py            # Package initialization
│   ├── api.py                 # FastAPI endpoints
│   ├── models.py              # Data models and schemas
│   └── scraper.py             # Core scraping functionality
├── main.py                    # CLI interface
├── ResourceScraper.jsx        # React component
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resource-scraper
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file:
   ```
   SERPER_API_KEY=your_serper_api_key_here
   ```
   Get your Serper API key from [serper.dev](https://serper.dev)

## Usage

### Command Line Interface

Run the CLI tool:
```bash
python main.py
```

The CLI provides an interactive interface to:
- Search for resources by topic
- Filter by resource type
- View detailed resource information
- See credibility and relevance scores

### API Server

1. **Start the server**
   ```bash
   uvicorn resource_scraper.api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **API Endpoints**

   - **GET `/api/resource-types`**
     Get available resource types
     ```bash
     curl http://localhost:8000/api/resource-types
     ```
     Response:
     ```json
     {
       "resource_types": [
         {"value": "video", "label": "Video"},
         {"value": "course", "label": "Course"},
         {"value": "documentation", "label": "Documentation"},
         {"value": "practice", "label": "Practice"},
         {"value": "other", "label": "Other"}
       ]
     }
     ```

   - **POST `/api/search`**
     Search for resources
     ```bash
     curl -X POST http://localhost:8000/api/search \
       -H "Content-Type: application/json" \
       -d '{
         "topic": "Python Programming",
         "resource_types": ["video", "documentation"]
       }'
     ```
     Response:
     ```json
     {
       "resources": [
         {
           "title": "Resource Title",
           "url": "https://resource-url.com",
           "description": "Resource description",
           "resource_type": "video",
           "source": "web_search",
           "credibility_score": 0.8,
           "relevance_score": 0.9,
           "votes": 0
         }
       ],
       "total_results": 1
     }
     ```

   - **GET `/health`**
     Check API health
     ```bash
     curl http://localhost:8000/health
     ```

### React Integration

1. **Install dependencies**
   ```bash
   npm install @mui/material @emotion/react @emotion/styled axios
   ```

2. **Import the component**
   ```jsx
   import ResourceScraper from './ResourceScraper';
   ```

3. **Use in your React app**
   ```jsx
   function App() {
     return (
       <div>
         <ResourceScraper />
       </div>
     );
   }
   ```

4. **Component Features**
   - Search interface
   - Resource type filtering
   - Beautiful resource cards
   - Rating display
   - Loading states
   - Error handling

### API Integration Examples

1. **JavaScript/TypeScript**
   ```typescript
   const API_BASE_URL = 'http://localhost:8000/api';

   // Search for resources
   const searchResources = async (topic: string, resourceTypes?: string[]) => {
     const response = await fetch(`${API_BASE_URL}/search`, {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ topic, resource_types: resourceTypes })
     });
     return await response.json();
   };
   ```

2. **Python**
   ```python
   import requests

   API_BASE_URL = 'http://localhost:8000/api'

   def search_resources(topic: str, resource_types: list = None) -> dict:
       response = requests.post(f'{API_BASE_URL}/search', json={
           'topic': topic,
           'resource_types': resource_types
       })
       return response.json()
   ```

## Development

### Core Components

1. **models.py**
   - Defines data structures
   - Resource types enumeration
   - Request/response models

2. **scraper.py**
   - Core scraping logic
   - Resource ranking algorithms
   - Credibility scoring

3. **api.py**
   - FastAPI endpoints
   - CORS configuration
   - Error handling

### Adding New Features

1. **New Resource Types**
   - Add to `ResourceType` enum in `models.py`
   - Update scraping logic in `scraper.py`

2. **Custom Scoring**
   - Modify `calculate_credibility_score` in `scraper.py`
   - Adjust relevance calculation in `search_resources`

## Production Deployment

1. **API Server**
   - Host on cloud platform (Heroku, AWS, GCP)
   - Set environment variables
   - Configure CORS for your domain
   - Add authentication if needed

2. **React Component**
   - Update `API_BASE_URL` to production URL
   - Build and deploy with your React app

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for your own educational purposes. 