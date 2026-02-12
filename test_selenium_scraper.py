#!/usr/bin/env python
"""Quick test of Selenium-based Zillow scraper."""

import sys
sys.path.insert(0, '/Users/alex/Documents/real-estate-analyzer')

from src.scraper.scraper import ZillowScraper, DemoScraper
import logging

logging.basicConfig(level=logging.INFO)

print("\n" + "="*60)
print("TESTING ENHANCED SELENIUM ZILLOW SCRAPER")
print("="*60 + "\n")

location = "San Francisco, CA"
print(f"Location: {location}\n")

# Test Zillow Scraper (with stealth)
print("→ Testing ZillowScraper (with stealth anti-bot bypass)...")
zillow = ZillowScraper(headless=True)
try:
    listings = zillow.scrape_listings(location)
    print(f"✓ Got {len(listings)} listings")
    if listings:
        print(f"  Source: {listings[0].get('source')}")
        print(f"  Sample: {listings[0].get('address')}, {listings[0].get('city')} - ${listings[0].get('price')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Demo Scraper for comparison
print("\n→ Testing DemoScraper (fallback)...")
demo = DemoScraper()
try:
    listings = demo.scrape_listings(location)
    print(f"✓ Got {len(listings)} listings")
    if listings:
        print(f"  Source: {listings[0].get('source')}")
        print(f"  Sample: {listings[0].get('address')}, {listings[0].get('city')} - ${listings[0].get('price')}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60 + "\n")
