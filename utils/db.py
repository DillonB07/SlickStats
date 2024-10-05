from dotenv import load_dotenv
from pymongo import MongoClient

from utils.env import env

from slack_sdk.oauth import InstallationStore
from slack_sdk.oauth.installation_store.models.installation import Installation

load_dotenv()

class MongoDBInstallationStore(InstallationStore):
    def __init__(self, mongo_uri, db_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.users = self.db.users


    def ping(self):
        data = self.client.server_info()
        if data:
            return True


    def save(self, installation: Installation):
        user_data = {
            "user_id": installation.user_id,
            "user_token": installation.user_token,
            "bot_token": installation.bot_token,
        }
        self.users.update_one(
            {"user_id": installation.user_id}, {"$set": user_data}, upsert=True
        )


    def find_user(self, user_id: str):
        return self.users.find_one({"user_id": user_id})


    def delete(self, user_id):
        self.users.delete_one({"user_id": user_id})


    def update_user_settings(self, user_id, data):
        self.users.update_one({"user_id": user_id}, {"$set": data}, upsert=True)


    def get_user_settings(self, user_id):
        return self.users.find_one({"user_id": user_id})


db_client = MongoDBInstallationStore(env.mongo_uri, "slickstats")