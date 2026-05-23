# config_server_db.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

def db_config(app) -> None:
    """  """
    # --- Configuration ---
    # Variable to set the environment
    is_pythonanywhere = 'PYTHONANYWHERE_DOMAIN' in os.environ
    raw_db_url = os.getenv('DATABASE_URL')

    if is_pythonanywhere:
        # 1. Deployment: PythonAnywhere uses SQLite
        basedir = os.path.abspath(os.path.dirname(__file__))
        DATABASE_URL = "sqlite:///" + os.path.join(basedir, "cypherware.db")
        print("LOG: Using SQLite (PythonAnywhere Environment)")

    elif raw_db_url:
        # 2. Local/Dev: PostgreSQL via environment variable
        DATABASE_URL = raw_db_url.replace("postgres://", "postgresql://", 1)
        print("LOG: Using PostgreSQL (Environment Variable Detected)")

    else:
        # 3. Critical Error: No DB configured
        print("ERROR: No database configuration found!")
        print("Ensure DATABASE_URL is set in your .env file for local development.")
        DATABASE_URL = None # This will cause SQLAlchemy to raise a helpful error on start

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL # The Connection String. This tells Flask exactly where to find your database.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # The Performance Toggle
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-cipher-123') # The Security Anchor. Important line for your JWT (JSON Web Token) implementation.
    
    return True #SQLAlchemy(app)

def check_db_connection(app, db):
    """Verifies the database connection on startup."""
    try:
        # We use a simple 'SELECT 1' to ping the database
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        print(f"✅ DB SUCCESS: Connected to DATABASE")
    except Exception as e:
        print(f"❌ DB ERROR: Could not connect to the database.")
        print(f"Details: {e}")
        # We don't exit here so the server can still serve static pages if needed,
        # but you'll see the loud error in your terminal.