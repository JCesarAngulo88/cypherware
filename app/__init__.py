# app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration - using your existing Secret Key
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "your-dev-key")
    
    # Initialize Extensions
    jwt = JWTManager(app)

    # REGISTER THE BLUEPRINT
    from app.routes.auth import auth_bp
    # url_prefix means your login becomes: http://127.0.0.1:5001/api/login
    app.register_blueprint(auth_bp, url_prefix='/api')

    return app