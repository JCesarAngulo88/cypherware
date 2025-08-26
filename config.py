import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/portfolio_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False