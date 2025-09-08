import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_URL")


class Config:
    DB_URL = db_url


config = Config
