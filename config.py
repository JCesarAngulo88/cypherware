import os

DRIVER_PATH = "/Users/jcesar/projects/cypherware-webapp/myenv/chromedriver"

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')