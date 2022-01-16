import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        """Constructor"""
        self.db_name = os.environ.get("DATABASE")
        self.user = os.environ.get("USER")
        self.password = os.environ.get("PASSWORD")
        self.port = os.environ.get("PORT")
        self.host = os.environ.get("HOST")