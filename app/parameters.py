import os

from dotenv import load_dotenv

load_dotenv()

DB_PG_NAME = os.environ.get("DB_PG_NAME")
DB_PG_PASSWORD = os.environ.get("DB_PG_PASSWORD")
DB_PG_NAME_DB = os.environ.get("DB_PG_NAME_DB")
DB_PG_HOST = os.environ.get("DB_PG_HOST")