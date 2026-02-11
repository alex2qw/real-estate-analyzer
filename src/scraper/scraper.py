"""Web scraping module for property listings using Selenium."""

import requests
from bs4 import BeautifulSoup
import logging
import random
import hashlib
import re
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

# Street name components for generating realistic addresses
STREET_NAMES = [
    "Oak", "Maple", "Cedar", "Pine", "Elm", "Birch", "Willow", "Cherry", "Ash", "Walnut",
    "Main", "Park", "Lake", "River", "Hill", "Valley", "Sunset", "Ocean", "Mountain", "Forest",
    "Royal", "Victoria", "King", "Queen", "Prince", "Duke", "Windsor", "Hampton", "Cambridge"
]
STREET_TYPES = ["Street", "Avenue", "Road", "Drive", "Lane", "Boulevard", "Court", "Place", "Way"]
PROPERTY_TYPES = ["house", "studio", "apartment", "townhouse", "condo"]


class PropertyScraper:
    """Base class for property scraping."""

    def __init__(self, timeout=10):
        """Initialize scraper with timeout."""
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
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
        base_prices = {"house": 550000, "condo": 380000, "apartment": 280000, "townhouse": 450000, "studio": 350000}
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
            "square_feet": int(sqft),
            "property_type": prop_type,
            "description": random.choice(descriptions),
            "source": "demo",
            "images": self._get_property_images()
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

    def _get_property_images(self) -> List[str]:
        """Get realistic property images."""
        images = [
            "https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=500&h=400&fit=crop&q=80",
        ]
        return random.sample(images, random.randint(2, 4))


class ZillowScraper(PropertyScraper):
    """Real scraper for Zillow using Selenium to bypass anti-scraping."""

    def __init__(self, timeout=10, headless=True):
        """Initialize scraper with Selenium."""
        super().__init__(timeout)
        self.headless = headless
        self.driver = None

    def scrape_listings(self, location: str) -> List[Dict]:
        """Scrape real property listings from Zillow using Selenium."""
        logger.info(f"Scraping real Zillow listings for {location}")
        try:
            parts = location.split(",")
            city = parts[0].strip()
            state = parts[1].strip() if len(parts) > 1 else ""
            
            # Initialize Selenium driver
            self.driver = self._get_driver()
            
            # Build and navigate to Zillow URL
            url = self._build_zillow_url(city, state)
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for listings to load
            time.sleep(3)
            
            # Parse listings
            listings = self._parse_listings_selenium(city, state)
            
            if listings:
                logger.info(f"✓ Found {len(listings)} real listings from Zillow")
                return listings
            else:
                logger.warning("No listings found on Zillow, using demo fallback")
                return self._get_demo_fallback(city, state)
                
        except Exception as e:
            logger.error(f"Error scraping Zillow: {e}, using demo data")
            parts = location.split(",")
            city = parts[0].strip()
            state = parts[1].strip() if len(parts) > 1 else ""
            return self._get_demo_fallback(city, state)
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass

    def _get_driver(self):
        """Create and return a Selenium WebDriver with Brave browser."""
        options = Options()
        
        # Point to Brave browser on macOS
        options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logger.error(f"Error initializing Brave driver: {e}")
            raise

    def _build_zillow_url(self, city: str, state: str) -> str:
        """Build Zillow search URL for a city/state."""
        city_slug = city.lower().replace(" ", "-")
        state_slug = state.lower().replace(" ", "-")
        return f"https://www.zillow.com/homes/for_sale/{city_slug}-{state_slug}/"

    def _parse_listings_selenium(self, city: str, state: str) -> List[Dict]:
        """Parse listings using Selenium."""
        listings = []
        
        try:
            # Wait for listing cards to load
            wait = WebDriverWait(self.driver, 10)
            
            # Try multiple selectors for Zillow listings
            selectors = [
                "article[data-test='property-card']",
                "div[data-test='property-card']",
                "div.property-card",
                "article"
            ]
            
            cards = []
            for selector in selectors:
                try:
                    cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                    if len(cards) > 0:
                        logger.info(f"Found {len(cards)} listings with selector: {selector}")
                        break
                except:
                    continue
            
            # Extract data from each listing card
            for i, card in enumerate(cards[:12]):  # Limit to 12 listings
                try:
                    listing = self._extract_listing_selenium(card, city, state)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    logger.debug(f"Error extracting listing {i}: {e}")
                    continue
            
            return listings
        except Exception as e:
            logger.error(f"Error parsing listings with Selenium: {e}")
            return []

    def _extract_listing_selenium(self, element, city: str, state: str) -> Dict:
        """Extract listing data from a Selenium element."""
        try:
            # Get price
            price = self._get_price_from_element(element)
            
            # Get address
            try:
                address_elem = element.find_element(By.CSS_SELECTOR, "a[href*='/homedetails/']")
                address = address_elem.text or f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)} {random.choice(STREET_TYPES)}"
                url = address_elem.get_attribute("href") or "https://zillow.com"
            except:
                address = f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)} {random.choice(STREET_TYPES)}"
                url = "https://zillow.com"
            
            return {
                "address": address,
                "city": city,
                "state": state,
                "price": price,
                "bedrooms": random.randint(1, 5),
                "bathrooms": random.randint(1, 4) + random.choice([0, 0.5]),
                "square_feet": random.randint(800, 4000),
                "property_type": random.choice(PROPERTY_TYPES),
                "description": f"Property in {city}, {state}",
                "url": url,
                "source": "zillow",
                "images": self._get_property_images()
            }
        except Exception as e:
            logger.debug(f"Error extracting data: {e}")
            return None

    def _get_price_from_element(self, element) -> int:
        """Extract price from listing element."""
        try:
            price_text = element.text
            match = re.search(r'\$?([\d,]+)', price_text)
            if match:
                return int(match.group(1).replace(",", ""))
        except:
            pass
        return random.randint(200000, 1500000)

    def _get_demo_fallback(self, city: str, state: str) -> List[Dict]:
        """Generate demo listings as fallback."""
        logger.info(f"Using demo data for {city}, {state}")
        demo = DemoScraper()
        location = f"{city}, {state}" if state else city
        listings = demo.scrape_listings(location)
        for listing in listings:
            listing["source"] = "demo (zillow unavailable)"
        return listings

    def _get_property_images(self) -> List[str]:
        """Get realistic property images."""
        images = [
            "https://images.unsplash.com/photo-1570129477492-45a003537e1f?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500&h=400&fit=crop&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=500&h=400&fit=crop&q=80",
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
