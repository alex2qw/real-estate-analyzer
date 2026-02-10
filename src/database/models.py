"""SQLAlchemy models for Real Estate Market Analyzer."""

from datetime import datetime
from src.app import db


class Property(db.Model):
    """Property listing model."""
    
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10))
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Float)
    square_feet = db.Column(db.Integer)
    property_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    source = db.Column(db.String(100))
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    price_history = db.relationship('PriceHistory', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Property {self.address}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'price': self.price,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'square_feet': self.square_feet,
            'property_type': self.property_type,
            'source': self.source,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
        }


class PriceHistory(db.Model):
    """Price history tracking for properties."""
    
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PriceHistory property_id={self.property_id} price={self.price}>'


class MarketReport(db.Model):
    """Generated market analysis reports."""
    
    __tablename__ = 'market_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    report_type = db.Column(db.String(50))
    average_price = db.Column(db.Float)
    median_price = db.Column(db.Float)
    price_trend = db.Column(db.String(20))
    market_heat = db.Column(db.String(20))
    total_listings = db.Column(db.Integer)
    report_data = db.Column(db.JSON)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MarketReport {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'average_price': self.average_price,
            'median_price': self.median_price,
            'price_trend': self.price_trend,
            'market_heat': self.market_heat,
            'total_listings': self.total_listings,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
        }
