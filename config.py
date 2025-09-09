import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://jcesar:Celrevo13974@localhost:5432/cypherware_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')