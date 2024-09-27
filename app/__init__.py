from flask import Flask
from .routes.tds import tds_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://pmmaturity.thouclabs.ai/backend"
    ]
    
    CORS(app, resources={r"/*": {"origins": allowed_origins, "headers": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]}})

    # Register blueprints
    app.register_blueprint(tds_bp, url_prefix='/api/tds')
    
    return app
