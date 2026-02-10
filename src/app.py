"""Flask application entry point for Real Estate Market Analyzer."""

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()


def create_app(config_name="development"):
    """Application factory function."""
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///real_estate.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from src.api.routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    # Routes
    @app.route("/")
    def index():
        """Dashboard home page."""
        return render_template("index.html")

    @app.route("/properties")
    def properties_page():
        """Properties listing page."""
        return render_template("properties.html")

    @app.route("/property/<int:property_id>")
    def property_detail(property_id):
        """Property detail page."""
        return render_template("property_detail.html")

    @app.route("/analytics")
    def analytics_page():
        """Analytics and charts page."""
        return render_template("analytics.html")

    @app.route("/scrape")
    def scrape_page():
        """Scrape data page."""
        return render_template("scrape.html")

    @app.route("/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
