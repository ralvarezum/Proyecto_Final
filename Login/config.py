from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    #SERVER_NAME = environ.get("SERVER_NAME")

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sites.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
