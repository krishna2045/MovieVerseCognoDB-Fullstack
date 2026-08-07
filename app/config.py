import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    """Common settings for all environments."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    COGNODB_URI = os.getenv('COGNODB_URI')
    COGNODB_PASSWORD = os.getenv('COGNODB_PASSWORD')
    COGNODB_USERNAME = os.getenv('COGNODB_USERNAME')
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(BaseConfig):
    ENV = 'production'
    # Additional production‑only settings can go here
