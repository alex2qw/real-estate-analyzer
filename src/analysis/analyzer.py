"""Market analysis module for price trends and statistics."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Analyze market trends and generate statistics."""

    def __init__(self, properties_df: pd.DataFrame):
        """Initialize analyzer with properties data."""
        self.df = properties_df

    def calculate_price_statistics(self) -> Dict:
        """Calculate price statistics."""
        return {
            "mean": float(self.df["price"].mean()),
            "median": float(self.df["price"].median()),
            "std": float(self.df["price"].std()),
            "min": float(self.df["price"].min()),
            "max": float(self.df["price"].max()),
            "count": len(self.df),
        }

    def calculate_price_trend(self, time_column: str = "scraped_at") -> Dict:
        """Calculate price trends over time."""
        df_sorted = self.df.sort_values(time_column)

        # Calculate weekly average prices
        df_sorted["week"] = pd.to_datetime(df_sorted[time_column]).dt.to_period("W")
        weekly_avg = df_sorted.groupby("week")["price"].mean()

        # Determine trend direction
        if len(weekly_avg) > 1:
            price_change = weekly_avg.iloc[-1] - weekly_avg.iloc[0]
            trend = "up" if price_change > 0 else "down"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "data": weekly_avg.to_dict(),
        }

    def calculate_market_heat(self) -> str:
        """Calculate market heat based on inventory and price trends."""
        # Simplified market heat calculation
        avg_price = self.df["price"].mean()

        if avg_price > 500000:
            return "hot"
        elif avg_price > 300000:
            return "warm"
        else:
            return "cool"

    def analyze_by_property_type(self) -> Dict:
        """Analyze market by property type."""
        results = {}

        for prop_type in self.df["property_type"].unique():
            type_df = self.df[self.df["property_type"] == prop_type]
            results[prop_type] = {
                "count": len(type_df),
                "avg_price": float(type_df["price"].mean()),
                "median_price": float(type_df["price"].median()),
            }

        return results

    def analyze_by_location(self) -> Dict:
        """Analyze market by location."""
        results = {}

        for city in self.df["city"].unique():
            city_df = self.df[self.df["city"] == city]
            results[city] = {
                "count": len(city_df),
                "avg_price": float(city_df["price"].mean()),
                "median_price": float(city_df["price"].median()),
            }

        return results

    def find_price_anomalies(self, threshold: float = 2.0) -> List[Dict]:
        """Find properties with anomalous prices."""
        mean = self.df["price"].mean()
        std = self.df["price"].std()

        anomalies = self.df[
            (self.df["price"] > mean + threshold * std)
            | (self.df["price"] < mean - threshold * std)
        ]

        return anomalies.to_dict("records")
