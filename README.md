# Real Estate Market Analyzer

A comprehensive web application for scraping property listings, analyzing price trends, and generating market reports with interactive visualizations.

## Features

- **Web Scraping**: Automated scraping of property listings from multiple real estate sources
- **Price Trend Analysis**: Track and analyze price trends over time
- **Market Reports**: Generate detailed market analysis reports by location, property type, and price range
- **Interactive Visualizations**: Plotly-based charts showing market trends, price distributions, and comparisons
- **Market Metrics**: Key performance indicators including average prices, price changes, market heat, etc.
- **Property Comparison**: Compare properties side-by-side with detailed analysis
- **Responsive Dashboard**: Modern, user-friendly web interface
- **RESTful API**: Access market data programmatically

## Tech Stack

- **Backend**: Flask
- **Database**: SQLAlchemy with SQLite
- **Web Scraping**: BeautifulSoup4, Requests, Selenium
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly
- **Frontend**: Bootstrap 5, JavaScript
- **Task Scheduling**: APScheduler (for automated scraping)

## Project Structure

```
real-estate-analyzer/
├── src/
│   ├── app.py                 # Flask application entry point
│   ├── database/
│   │   ├── db.py             # Database initialization and session management
│   │   └── models.py         # SQLAlchemy models
│   ├── scraper/
│   │   ├── scraper.py        # Web scraping logic
│   │   ├── parsers.py        # HTML parsing utilities
│   │   └── sources.py        # Data source configurations
│   ├── analysis/
│   │   ├── analyzer.py       # Price trend and market analysis
│   │   └── reports.py        # Report generation
│   ├── visualization/
│   │   └── charts.py         # Plotly visualization functions
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css    # Custom styling
│   │   └── js/
│   │       └── main.js       # Client-side JavaScript
│   └── templates/
│       ├── base.html         # Base template
│       ├── index.html        # Dashboard
│       ├── market_analysis.html
│       ├── property_comparison.html
│       ├── reports.html
│       └── admin.html        # Admin panel
├── requirements.txt
├── config.py                 # Configuration settings
├── .env.example              # Environment variables template
├── init_db.py               # Database initialization script
├── run.py                   # Application runner
└── docker-compose.yml       # Docker setup
```

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd real-estate-analyzer
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize database

```bash
python init_db.py
```

### 6. Run the application

```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Usage

### Dashboard

The main dashboard displays:
- Market overview (total properties, average price, market trends)
- Recent listings
- Price distribution charts
- Market heat by location

### Market Analysis

Detailed analysis including:
- Price trends over time
- Median and average prices by location
- Price predictions (future trend analysis)
- Market comparisons between neighborhoods

### Property Comparison

Compare multiple properties with:
- Side-by-side feature comparison
- Price vs. value analysis
- Similar property suggestions

### Reports

Generate PDF/HTML reports for:
- Market summaries
- Investment opportunities
- Neighborhood analysis
- Price forecasts

### Admin Panel

Manage:
- Scraping schedules
- Data sources
- Database cleanup
- Manual scraping triggers

## API Endpoints

### Properties
- `GET /api/properties` - List all properties with filters
- `GET /api/properties/<id>` - Get property details
- `GET /api/properties/search?query=` - Search properties

### Market Data
- `GET /api/market/trends` - Price trends
- `GET /api/market/stats` - Market statistics
- `GET /api/market/heatmap` - Market heat by location
- `GET /api/market/forecast` - Price forecasts

### Analysis
- `GET /api/analysis/location/<location>` - Location analysis
- `GET /api/analysis/compare?ids=1,2,3` - Compare properties

## Scheduled Tasks

The application includes automated tasks:
- **Hourly**: Scrape new listings from configured sources
- **Daily**: Analyze price trends and update market metrics
- **Weekly**: Generate market reports

## Data Sources

Configure scrapers for:
- Zillow
- Redfin
- Realtor.com
- Local MLS databases
- Custom real estate websites

## Development

### Running in debug mode

```bash
export FLASK_ENV=development
python run.py
```

### Running tests

```bash
pytest tests/
```

### Building with Docker

```bash
docker-compose build
docker-compose up
```

## Database

The application uses SQLite by default. To use PostgreSQL:

1. Install PostgreSQL
2. Update `config.py` with PostgreSQL connection string
3. Run migrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an GitHub issue.

## Roadmap

- [ ] Machine learning price predictions
- [ ] Advanced filtering and search
- [ ] Email alerts for new listings
- [ ] User accounts and favorites
- [ ] Property investment ROI calculator
- [ ] Neighborhood comparisons
- [ ] Photo gallery and virtual tours
- [ ] Mobile app
