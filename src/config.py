import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(Config):
    TESTING = False
    SECRET_KEY = "n#$>94JAb;_}@hRMeYLE6"
    SQLALCHEMY_DATABASE_URI = "postgresql://felipe:w3ATnTZrE3lRqT2qPxWvCo4yBZDaExEM@dpg-crbdrnjtq21c73chjrjg-a.oregon-postgres.render.com:5432/fbank"
    JWT_SECRET_KEY = "Y5n;g[cmCK9Z:.t/s{,yWN"


class DevelopmentConfig(Config):
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///fbank.sqlite"
    JWT_SECRET_KEY = "super-secret"
    TESTING = False


class TestingConfig(Config):
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test"
    TESTING = True
