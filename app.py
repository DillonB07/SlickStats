from utils.db import db_client
from utils.update import update_status
from utils.slack import app
from utils.views import generate_home_view
from utils.env import env


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    print(event["user"])
    try:
        user_data = (
            db_client.find_user(user_id=event["user"]) or {"user_id": event["user"]}
        )
        print(user_data)
        client.views_publish(
            user_id=event["user"],
            token=user_data.get("user_token"),
            view=generate_home_view(
                user_data.get("lastfm_username", None),
                user_data.get("lastfm_api_key", None),
                user_data.get("steam_id", None),
                user_data.get("steam_api_key", None),
            ),
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("submit_settings")
def submit_settings(ack, body, logger):
    ack()
    settings = ["lastfm_username", "lastfm_api_key", "steam_id", "steam_api_key"]
    data = {}
    for block in body["view"]["state"]["values"].values():
        for setting in settings:
            if setting in block:
                data[setting] = block[setting]["value"]

    db_client.update_user_settings(body["user"]["id"], data)


if __name__ == "__main__":
    db_client.ping()
    print("Connected to MongoDB")
    update_status()
    app.start(port=env.port)
