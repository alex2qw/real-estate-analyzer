"""API routes for Real Estate Market Analyzer."""

from flask import Blueprint, jsonify, request
from src.database.models import Property, MarketReport
from src.app import db
from sqlalchemy import func

api_bp = Blueprint('api', __name__)


@api_bp.route('/properties', methods=['GET'])
def get_properties():
    """Get all properties with optional filtering."""
    # Get query parameters
    city = request.args.get('city')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    property_type = request.args.get('property_type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query
    query = Property.query
    
    if city:
        query = query.filter_by(city=city)
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if property_type:
        query = query.filter_by(property_type=property_type)
    
    # Paginate
    paginated = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page,
        'properties': [p.to_dict() for p in paginated.items],
    }), 200


@api_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """Get a specific property."""
    property_obj = Property.query.get_or_404(property_id)
    return jsonify(property_obj.to_dict()), 200


@api_bp.route('/properties', methods=['POST'])
def create_property():
    """Create a new property listing."""
    data = request.get_json()
    
    try:
        new_property = Property(
            url=data['url'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            price=data['price'],
            bedrooms=data.get('bedrooms'),
            bathrooms=data.get('bathrooms'),
            square_feet=data.get('square_feet'),
            property_type=data.get('property_type'),
            source=data.get('source'),
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        return jsonify(new_property.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/market/summary', methods=['GET'])
def market_summary():
    """Get market summary statistics."""
    location = request.args.get('city')
    
    query = Property.query
    if location:
        query = query.filter_by(city=location)
    
    total = query.count()
    avg_price = db.session.query(func.avg(Property.price)).filter_by(city=location).scalar() if location else None
    
    return jsonify({
        'total_listings': total,
        'average_price': avg_price,
        'location': location,
    }), 200


@api_bp.route('/reports', methods=['GET'])
def get_reports():
    """Get all market reports."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    paginated = MarketReport.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': paginated.total,
        'reports': [r.to_dict() for r in paginated.items],
    }), 200


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200
