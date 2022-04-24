import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    DB_USER = os.environ.get("DB_USER")
    SECRET_KEY = os.environ['SECRET_KEY']
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_SERVICE = os.environ.get("DB_SERVICE")
    DB_PORT = os.environ.get("DB_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'oracle+cx_oracle://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}'

