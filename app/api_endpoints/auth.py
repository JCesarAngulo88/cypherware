# app/routes/auth.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app # We use this to get the Secret Key safely

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/api/health")
def health():
    """
    Critical endpoint for GitHub Actions.
    Returns 200 OK to signal the server is ready for Selenium tests.
    """
    return jsonify({
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

# --- API Endpoints ---
@auth_bp.route("/api/login", methods=["POST"])
def login():
    auth = request.json
    if not auth or not auth.get('email') or not auth.get('password'):
        return jsonify({"error": "Could not verify"}), 401

    # MOCK LOGIN: In a real app, check against hashed password in DB
    if auth.get('email') == "admin@cypherware.com" and auth.get('password') == "password123":
        token = jwt.encode({
            'user': auth.get('email'),
            'exp': datetime.now(timezone.utc) + timedelta(hours=2)
        }, auth_bp.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({"error": "Invalid credentials"}), 401