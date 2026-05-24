import os
from dotenv import load_dotenv # Updated for windows

DRIVER_PATH = "/Users/julioangulo/Projects/cypherware/.venv/chromedriver"
from pathlib import Path

CHROME_BINARY_PATH = str(
    Path(
        "/Users/julioangulo/Applications/chrome-mac-arm64/"
        "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    )
)

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')