from db import db_client, update_user_settings, update_cache
import os
import views
from lastfm import update_lastfm_status
from slack import app
from views import generate_home_view


@app.message("hello")
def greetings(message, say):
    user = message["user"]
    say(f"Hello, <@{user}>!")


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        user_data = db_client.slickstats.users.find_one({"user_id": event["user"]})
        client.views_publish(
            user_id=event["user"],
            view=generate_home_view(
                user_data.get("lastfm_username", None),
                user_data.get("lastfm_api_key", None)
            )
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("submit_settings")
def submit_settings(ack, body, logger):
    ack()
    api_key = ""
    settings = ["lastfm_username", "lastfm_api_key"]
    data = {}
    for block in body["view"]["state"]["values"].values():
        for setting in settings:
            if setting in block:
                data[setting] = block[setting]["value"]
                api_key = block[setting]["value"]

    update_user_settings(
        body["user"]["id"],
        data
    )


if __name__ == '__main__':
    db_client.admin.command("ping")
    print("Connected to MongoDB")
    update_cache()
    update_lastfm_status()
    app.start(port=int(os.environ.get("PORT", 3000)))
