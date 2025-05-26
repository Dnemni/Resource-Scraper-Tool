import os
import json
import httpx
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from .models import Resource, ResourceType
from dotenv import load_dotenv

load_dotenv()

class ResourceScraper:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        
    async def search_serper(self, query: str) -> Dict[str, Any]:
        """Search using Serper API"""
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 20
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://google.serper.dev/search",
                headers=headers,
                json=payload
            )
            return response.json()

    def calculate_credibility_score(self, url: str, title: str, description: str) -> float:
        """Calculate credibility score based on domain and content"""
        score = 0.0
        
        # Trusted educational domains
        trusted_domains = [
            "edu", "khan", "coursera", "udacity", "edx",
            "mit.edu", "stanford.edu", "youtube.com",
            "docs.python.org", "developer.mozilla.org"
        ]
        
        for domain in trusted_domains:
            if domain in url.lower():
                score += 0.3
                break
                
        # Check for educational indicators in title/description
        edu_keywords = ["course", "tutorial", "learn", "education", "lecture", "lesson"]
        for keyword in edu_keywords:
            if keyword in title.lower() or keyword in description.lower():
                score += 0.1
                
        return min(1.0, score + 0.2)  # Base score of 0.2

    def determine_resource_type(self, url: str, title: str) -> ResourceType:
        """Determine the type of resource based on URL and title"""
        url_lower = url.lower()
        title_lower = title.lower()
        
        if "youtube.com" in url_lower or "youtu.be" in url_lower:
            return ResourceType.VIDEO
        elif any(x in url_lower for x in ["coursera", "edx", "udacity", "khan"]):
            return ResourceType.COURSE
        elif any(x in url_lower for x in ["docs.", "documentation", "guide"]):
            return ResourceType.DOCUMENTATION
        elif any(x in url_lower for x in ["leetcode", "hackerrank", "quizlet", "practice"]):
            return ResourceType.PRACTICE
        else:
            return ResourceType.OTHER

    async def search_resources(self, topic: str) -> List[Resource]:
        """Main method to search and process educational resources"""
        search_query = f"{topic} tutorial education course"
        results = await self.search_serper(search_query)
        
        resources = []
        
        # Process organic search results
        for result in results.get("organic", []):
            url = result.get("link")
            title = result.get("title", "")
            description = result.get("snippet", "")
            
            resource_type = self.determine_resource_type(url, title)
            credibility_score = self.calculate_credibility_score(url, title, description)
            
            # Calculate simple relevance score based on keyword matching
            relevance_score = sum(1 for word in topic.lower().split() 
                                if word in title.lower() or word in description.lower()) / len(topic.split())
            relevance_score = min(1.0, relevance_score)
            
            resource = Resource(
                title=title,
                url=url,
                description=description,
                resource_type=resource_type.value,
                source="web_search",
                credibility_score=credibility_score,
                relevance_score=relevance_score
            )
            resources.append(resource)
        
        # Sort resources by combined score
        resources.sort(key=lambda x: (x.credibility_score + x.relevance_score) / 2, reverse=True)
        return resources 