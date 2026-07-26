import os


class Config:
    """Base configuration"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "products")

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


def get_config():
    if os.getenv("FLASK_ENV") == "production":
        return ProductionConfig
    return DevelopmentConfig