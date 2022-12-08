"""Application Models"""
import bson

from werkzeug.security import generate_password_hash, check_password_hash
from models.model import BaseModel

from helpers.token import set_token


class User(BaseModel):
    """User Model"""

    #Se podria desacoplar de esta clase la forma en que se genera el password

    def __init__(self):
        super().__init__()


    def create(self, name="", email="", password="", endpoint="", role="greenhouse"):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            raise Exception("User {0} already exists".format(email))
        new_user = self.db.users.insert_one(
            {
                "name": name,
                "email": email,
                "password": self.__encrypt_password(password),
                "active": True,
                "role": role,
                "endpoint": endpoint
            }
        )
        return self.get_by_id(new_user.inserted_id)

    def get_all(self):
        """Get all users"""
        users = self.db.users.find({"active": True})
        return [{**user, "_id": str(user["_id"])} for user in users]

    def findAll(self, conditions: dict = {}) -> list:
        users = self.db.users.find({
            **conditions,
            "active": True
        })
        return [{
            "_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            #"role": user["role"]
        } for user in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = self.db.users.find_one({"_id": bson.ObjectId(user_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user

    def get_by_email(self, email):
        """Get a user by email"""
        user = self.db.users.find_one({"email": email, "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update(self, user_id, name=""):
        """Update a user"""
        data = {}
        if name:
            data["name"] = name
        user = self.db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user

    def disable_account(self, user_id):
        """Disable a user account"""
        user = self.db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user

    @staticmethod
    def __encrypt_password(password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        
        if not user or not check_password_hash(user["password"], password):
            raise Exception("Invalid email or password")

        user.pop("password")

        user = set_token(user)

        return user
