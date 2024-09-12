from db import db_client
import os
import views
from lastfm import update_lastfm_status
from slack import app
from server import flask_app
from views import generate_home_view


@app.message("hello")
def greetings(message, say):
    user = message["user"]
    say(f"Hello, <@{user}>!")


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    generate_home_view(event["user"], client),


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

    db_client.update_user_settings(body["user"]["id"], data)


if __name__ == "__main__":
    db_client.update_cache()
    update_lastfm_status()
    flask_app.run(port=int(os.environ.get("PORT", 3000)))
