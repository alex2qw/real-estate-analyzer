"""Test API endpoints."""

import pytest
from src.app import create_app, db
from src.database.models import Property


@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_properties_empty(client):
    """Test getting properties when none exist."""
    response = client.get("/api/properties")
    assert response.status_code == 200
    assert response.json["total"] == 0


def test_create_property(client, app):
    """Test creating a property."""
    data = {
        "url": "http://example.com/property1",
        "address": "123 Main St",
        "city": "New York",
        "state": "NY",
        "price": 500000,
        "bedrooms": 3,
        "bathrooms": 2,
        "square_feet": 2000,
        "property_type": "house",
        "source": "test",
    }

    response = client.post("/api/properties", json=data)
    assert response.status_code == 201
    assert response.json["address"] == "123 Main St"


def test_market_summary(client, app):
    """Test market summary endpoint."""
    # Create a test property
    with app.app_context():
        prop = Property(
            url="http://example.com/prop1",
            address="123 Main St",
            city="New York",
            state="NY",
            price=500000,
        )
        db.session.add(prop)
        db.session.commit()

    response = client.get("/api/market/summary?city=New York")
    assert response.status_code == 200
    assert response.json["total_listings"] >= 0
