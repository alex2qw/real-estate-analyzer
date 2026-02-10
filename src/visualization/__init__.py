"""Visualization module for charts and reports."""

import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import pandas as pd


class ChartGenerator:
    """Generate interactive charts using Plotly."""

    @staticmethod
    def price_trend_chart(data: Dict) -> str:
        """Generate price trend chart."""
        df = pd.DataFrame(data)

        fig = px.line(
            df,
            x="date",
            y="price",
            title="Price Trends Over Time",
            labels={"price": "Average Price ($)", "date": "Date"},
        )

        return fig.to_html(include_plotlyjs="cdn")

    @staticmethod
    def price_distribution_chart(prices: List[float]) -> str:
        """Generate price distribution histogram."""
        fig = px.histogram(
            x=prices,
            nbins=50,
            title="Property Price Distribution",
            labels={"x": "Price ($)", "count": "Number of Properties"},
        )

        return fig.to_html(include_plotlyjs="cdn")

    @staticmethod
    def property_type_comparison(data: Dict) -> str:
        """Generate property type comparison chart."""
        types = list(data.keys())
        prices = [v["avg_price"] for v in data.values()]

        fig = px.bar(
            x=types,
            y=prices,
            title="Average Price by Property Type",
            labels={"y": "Average Price ($)", "x": "Property Type"},
        )

        return fig.to_html(include_plotlyjs="cdn")

    @staticmethod
    def location_comparison(data: Dict) -> str:
        """Generate location comparison chart."""
        locations = list(data.keys())
        prices = [v["avg_price"] for v in data.values()]
        counts = [v["count"] for v in data.values()]

        fig = go.Figure(
            data=[
                go.Bar(name="Average Price", x=locations, y=prices, yaxis="y"),
                go.Bar(name="Listings", x=locations, y=counts, yaxis="y2"),
            ]
        )

        fig.update_layout(
            title="Market Comparison by Location",
            yaxis={"title": "Average Price ($)"},
            yaxis2={"title": "Number of Listings", "overlaying": "y", "side": "right"},
        )

        return fig.to_html(include_plotlyjs="cdn")
