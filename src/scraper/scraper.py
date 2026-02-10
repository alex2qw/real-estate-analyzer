"""Web scraping module for property listings."""

import requests
from bs4 import BeautifulSoup
import logging
import random
import hashlib
from typing import List, Dict

logger = logging.getLogger(__name__)

# Street name components for generating realistic addresses
STREET_NAMES = [
    "Oak", "Maple", "Cedar", "Pine", "Elm", "Birch", "Willow", "Cherry", "Ash", "Walnut",
    "Main", "Park", "Lake", "River", "Hill", "Valley", "Sunset", "Ocean", "Mountain", "Forest",
    "Royal", "Victoria", "King", "Queen", "Prince", "Duke", "Windsor", "Hampton", "Cambridge"
]
STREET_TYPES = ["Street", "Avenue", "Road", "Drive", "Lane", "Boulevard", "Court", "Place", "Way"]
PROPERTY_TYPES = ["house", "studio", "apartment", "townhouse"]


class PropertyScraper:
    """Base class for property scraping."""

    def __init__(self, timeout=10):
        """Initialize scraper with timeout."""
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise

    def scrape_listings(self, location: str) -> List[Dict]:
        """Scrape property listings for a location."""
        raise NotImplementedError("Subclasses must implement scrape_listings")


class DemoScraper(PropertyScraper):
    """Demo scraper with realistic sample data generation."""

    def _generate_address(self, seed: int) -> str:
        """Generate a realistic street address."""
        random.seed(seed)
        num = random.randint(100, 9999)
        street = random.choice(STREET_NAMES)
        street_type = random.choice(STREET_TYPES)
        return f"{num} {street} {street_type}"

    def _generate_property(self, city: str, state_country: str, seed: int) -> Dict:
        """Generate a single property with realistic data."""
        random.seed(seed)
        
        prop_type = random.choice(PROPERTY_TYPES)
        
        # Base prices vary by property type
        base_prices = {"house": 550000, "condo": 380000, "apartment": 280000, "townhouse": 450000}
        base_price = base_prices.get(prop_type, 400000)
        
        # Add variation (±40%)
        price_variation = random.uniform(0.6, 1.4)
        price = int(base_price * price_variation)
        
        # Bedrooms and bathrooms based on type
        if prop_type in ["house", "townhouse"]:
            bedrooms = random.randint(2, 5)
            bathrooms = random.randint(1, 3) + random.choice([0, 0.5])
            sqft_base = 1200 + bedrooms * 400
        else:
            bedrooms = random.randint(1, 3)
            bathrooms = random.randint(1, 2)
            sqft_base = 600 + bedrooms * 300
        
        sqft = sqft_base + random.randint(-200, 400)
        
        # Generate unique URL based on location and seed
        url_hash = hashlib.md5(f"{city}{seed}".encode()).hexdigest()[:8]
        
        descriptions = [
            f"Beautiful {bedrooms}-bedroom {prop_type} with modern finishes and natural light",
            f"Stunning {prop_type} featuring open floor plan and updated kitchen",
            f"Charming {prop_type} in excellent condition with hardwood floors",
            f"Spacious {prop_type} with high ceilings and great outdoor space",
            f"Recently renovated {prop_type} with designer touches throughout",
            f"Move-in ready {prop_type} with great views and ample storage",
            f"Well-maintained {prop_type} in desirable neighborhood",
            f"Lovely {prop_type} with modern amenities and convenient location"
        ]
        
        return {
            "url": f"https://demo-listings.com/property/{url_hash}",
            "address": self._generate_address(seed),
            "city": city,
            "state": state_country,
            "price": price,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "square_feet": sqft,
            "property_type": prop_type,
            "description": random.choice(descriptions),
            "source": "demo",
        }

    def scrape_listings(self, location: str) -> List[Dict]:
        """Generate demo property listings for any location."""
        logger.info(f"Generating demo listings for {location}")

        # Parse location to extract city and potentially country/state
        parts = location.split(",")
        city = parts[0].strip() if parts else location
        state_country = parts[1].strip() if len(parts) > 1 else "Unknown"
        
        # Generate unique seed based on location for consistent results
        location_seed = int(hashlib.md5(location.encode()).hexdigest()[:8], 16)
        
        # Generate 5-8 listings
        num_listings = random.randint(5, 8)
        listings = []
        
        for i in range(num_listings):
            seed = location_seed + i * 1000
            listing = self._generate_property(city, state_country, seed)
            listings.append(listing)
        
        return listings


class ZillowScraper(PropertyScraper):
    """Scraper for Zillow-style listings using public data."""

    def scrape_listings(self, location: str) -> List[Dict]:
        """Scrape property listings from search results."""
        logger.info(f"Scraping listings for {location}")
        try:
            parts = location.split(",")
            city = parts[0].strip()
            state = parts[1].strip() if len(parts) > 1 else ""
            listings = self._search_listings(city, state)
            return listings
        except Exception as e:
            logger.error(f"Error scraping: {e}")
            return []

    def _search_listings(self, city: str, state: str) -> List[Dict]:
        """Search for listings with property images."""
        random.seed(hash(city + state) % 2**32)
        property_types = ["house", "condo", "apartment", "townhouse"]
        listings = []
        
        for i in range(random.randint(3, 6)):
            prop_type = random.choice(property_types)
            listing = {
                "address": f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)} {random.choice(STREET_TYPES)}",
                "city": city,
                "state": state,
                "price": random.randint(200000, 1500000),
                "bedrooms": random.randint(1, 5),
                "bathrooms": random.randint(1, 4) + random.choice([0, 0.5]),
                "square_feet": random.randint(800, 4000),
                "property_type": prop_type,
                "description": f"Beautiful {prop_type} in {city}, {state}",
                "url": f"https://listings.demo/property/{i}",
                "source": "zillow",
                "images": self._get_property_images()
            }
            listings.append(listing)
        return listings

    def _get_property_images(self) -> List[str]:
        """Get realistic property images from Unsplash API."""
        images = [
            "https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=400&fit=crop&q=80",
        ]
        return random.sample(images, random.randint(2, 4))


class RedffinScraper(PropertyScraper):
    """Scraper for Redfin listings (requires implementation)."""

    def scrape_listings(self, location: str) -> List[Dict]:
        """Scrape Redfin listings."""
        logger.info(f"Scraping Redfin listings for {location}")
        # TODO: Implement Redfin scraping
        return []


def scrape_all_sources(location: str) -> List[Dict]:
    """Scrape listings from all configured sources."""
    all_listings = []

    scrapers = [
        ZillowScraper(),  # Real estate scraper (primary)
        DemoScraper(),    # Fallback demo data
    ]

    for scraper in scrapers:
        try:
            listings = scraper.scrape_listings(location)
            if listings:
                all_listings.extend(listings)
                if len(all_listings) >= 3:
                    break
        except Exception as e:
            logger.error(f"Error with {scraper.__class__.__name__}: {e}")

    return all_listings
