import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  Card,
  CardContent,
  Checkbox,
  CircularProgress,
  FormControl,
  FormControlLabel,
  FormGroup,
  TextField,
  Typography,
  Alert,
  Chip,
  Link,
  Rating,
} from '@mui/material';

const API_BASE_URL = 'http://localhost:8000/api'; // Change this to your API URL in production

const ResourceCard = ({ resource }) => {
  const score = (resource.credibility_score + resource.relevance_score) / 2;
  
  return (
    <Card sx={{ mb: 2, '&:hover': { boxShadow: 6 } }}>
      <CardContent>
        <Typography variant="h6" component="div" gutterBottom>
          {resource.title}
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Chip 
            label={resource.resource_type}
            color="primary"
            size="small"
            sx={{ mr: 2 }}
          />
          <Rating 
            value={score * 5}
            precision={0.5}
            readOnly
          />
        </Box>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          {resource.description}
        </Typography>
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link href={resource.url} target="_blank" rel="noopener noreferrer">
            Visit Resource
          </Link>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Credibility: {(resource.credibility_score * 100).toFixed(0)}%
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ ml: 2 }}>
              Relevance: {(resource.relevance_score * 100).toFixed(0)}%
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

const ResourceScraper = () => {
  const [topic, setTopic] = useState('');
  const [resourceTypes, setResourceTypes] = useState([]);
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch available resource types on component mount
  useEffect(() => {
    const fetchResourceTypes = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/resource-types`);
        setResourceTypes(response.data.resource_types);
      } catch (err) {
        console.error('Error fetching resource types:', err);
        setError('Failed to load resource types');
      }
    };
    
    fetchResourceTypes();
  }, []);

  const handleTypeChange = (value) => {
    setSelectedTypes(prev => 
      prev.includes(value)
        ? prev.filter(t => t !== value)
        : [...prev, value]
    );
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/search`, {
        topic: topic,
        resource_types: selectedTypes.length > 0 ? selectedTypes : null
      });
      
      setResources(response.data.resources);
    } catch (err) {
      console.error('Error searching resources:', err);
      setError('Failed to fetch resources. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Find Educational Resources
      </Typography>
      
      <form onSubmit={handleSearch}>
        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            label="Enter topic or course name"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            variant="outlined"
            sx={{ mb: 2 }}
          />
          
          <FormControl component="fieldset" variant="standard">
            <Typography variant="subtitle2" gutterBottom>
              Resource Types (Optional)
            </Typography>
            <FormGroup row>
              {resourceTypes.map(type => (
                <FormControlLabel
                  key={type.value}
                  control={
                    <Checkbox
                      checked={selectedTypes.includes(type.value)}
                      onChange={() => handleTypeChange(type.value)}
                    />
                  }
                  label={type.label}
                />
              ))}
            </FormGroup>
          </FormControl>
        </Box>
        
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading || !topic.trim()}
          fullWidth
        >
          {loading ? <CircularProgress size={24} /> : 'Search Resources'}
        </Button>
      </form>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ mt: 4 }}>
        {resources.length > 0 && (
          <Typography variant="h6" gutterBottom>
            Found {resources.length} resources for "{topic}"
          </Typography>
        )}
        
        {resources.map((resource, index) => (
          <ResourceCard key={index} resource={resource} />
        ))}
      </Box>
    </Box>
  );
};

export default ResourceScraper; 