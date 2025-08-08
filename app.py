# app.py
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.DEBUG)

# SQLAlchemy base class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# App factory
def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SESSION_SECRET")

    # Proxy fix for Render
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from routes import main as routes_blueprint
    app.register_blueprint(routes_blueprint)

    with app.app_context():
        import models  # Ensure models are loaded
        db.create_all()
        logging.info("Database tables created")

    return app
