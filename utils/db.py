from utils.env import env


def update_user_settings(user_id, data):
    client = env.mongo_client
    db = client["slickstats"]
    users = db.users
    users.update_one({"user_id": user_id}, {"$set": data}, upsert=True)


def get_all_users():
    client = env.mongo_client
    db = client["slickstats"]
    users = db.users
    return users.find()


def get_user_settings(user_id):
    client = env.mongo_client
    db = client["slickstats"]
    users = db.users
    return users.find_one({"user_id": user_id})
