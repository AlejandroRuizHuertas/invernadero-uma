import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient


class BaseModel:

    def __init__(self):
        self.DATABASE_URL = os.environ.get('DATABASE_URL')

        self.DATABASE_NAME = os.environ.get('DATABASE_NAME')

        self.client = MongoClient(self.DATABASE_URL)

        self.db = self.client[self.DATABASE_NAME]

    def insert(self, data: dict) -> dict | bool:
        pass

    def find(self, id: ObjectId) -> dict:
        pass

    def findAll(self, conditions: dict = {}) -> list:
        pass