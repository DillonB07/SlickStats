from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import json
import os


load_dotenv()

db_client = MongoClient(os.environ.get("MONGO_URI"), server_api=ServerApi("1"))


def update_user_settings(user_id, data):
    db_client.slickstats.users.update_one(
        {"user_id": user_id}, {"$set": data}, upsert=True
    )
    update_cache()


def get_user_settings(user_id):
    return db_client.slickstats.users.find_one({"user_id": user_id})


def update_cache():
    # fetch all data from users db
    users = db_client.slickstats.users.find({})
    data = []

    for user in users:
        user["_id"] = str(user["_id"])
        data.append(user)

    with open("cache.json", "w") as f:
        json.dump(data, f)
