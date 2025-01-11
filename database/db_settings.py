from dotenv import load_dotenv 
import os 

load_dotenv() 
DB_NAME = os.environ.get("DB_NAME") 
DB_USER=os.environ.get("DB_USER") 
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
""" TEST_DB_USER=os.environ.get("TEST_DB_USER") 
TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME") """