"""Quick Start Guide for Real Estate Market Analyzer."""

# Real Estate Market Analyzer - Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/real-estate-analyzer.git
cd real-estate-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

## Running the Application

```bash
# Start the Flask development server
python -m flask run

# Or use the Makefile
make run
```

Visit `http://localhost:5000` in your browser.

## API Usage

### Get Properties

```bash
# Get all properties
curl http://localhost:5000/api/properties

# Filter by city and price
curl http://localhost:5000/api/properties?city=New%20York&min_price=300000&max_price=500000

# Get specific property
curl http://localhost:5000/api/properties/1
```

### Create Property

```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://example.com/property",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "price": 500000,
    "bedrooms": 3,
    "bathrooms": 2,
    "square_feet": 2000,
    "property_type": "house",
    "source": "zillow"
  }'
```

### Market Summary

```bash
# Get market summary for a location
curl http://localhost:5000/api/market/summary?city=New%20York
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_api.py
```

## Code Quality

```bash
# Lint code
flake8 src

# Format code
black src

# Type check
mypy src
```

## Docker

```bash
# Build Docker image
docker build -t real-estate-analyzer .

# Run with Docker
docker run -p 5000:5000 real-estate-analyzer

# Run with Docker Compose
docker-compose up
```

## Project Structure

```
real-estate-analyzer/
├── src/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration
│   ├── database/
│   │   ├── models.py          # SQLAlchemy models
│   │   └── __init__.py
│   ├── scraper/
│   │   ├── scraper.py         # Web scraping logic
│   │   └── __init__.py
│   ├── analysis/
│   │   ├── analyzer.py        # Market analysis
│   │   └── __init__.py
│   ├── visualization/
│   │   └── __init__.py        # Chart generation
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   │   └── __init__.py
│   └── static/
├── tests/
│   ├── test_api.py
│   └── __init__.py
├── requirements.txt
├── README.md
├── DEPLOYMENT.md
└── Makefile
```

## Environment Variables

Key environment variables (see `.env.example`):

- `FLASK_ENV` - Environment (development/production)
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string
- `SCRAPER_TIMEOUT` - Scraping timeout in seconds

## Troubleshooting

### Port already in use
```bash
# Change port
python -m flask run --port 5001
```

### Database errors
```bash
# Reset database
rm real_estate.db
python -m flask run
```

### Missing dependencies
```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

1. Configure data sources for scraping
2. Implement advanced analysis features
3. Create frontend dashboard
4. Set up automated scraping schedule
5. Deploy to production

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

For issues and questions, please open a GitHub issue.
