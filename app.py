from slack_sdk import WebClient

from utils.db import get_user_settings
from utils.db import update_user_settings
from utils.env import env
from utils.slack import app
from utils.update import update_status
from utils.views import generate_home_view


@app.event("app_home_opened")
def update_home_tab(client: WebClient, event, logger):
    """

    :param client: WebClient:
    :param event:
    :param logger:

    """
    try:
        user_data = get_user_settings(user_id=event["user"]) or {
            "user_id": event["user"]
        }

        team_id = client.team_info()["team"]["id"]
        installations = env.installation_store.find_installations(team_id=team_id)
        if not installations:
            return
        installation = installations[0]
        token = installation.bot_token
        client.views_publish(
            user_id=event["user"],
            token=token,
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
    """

    :param ack:
    :param body:
    :param logger:

    """
    ack()
    settings = ["lastfm_username", "lastfm_api_key", "steam_id", "steam_api_key"]
    data = {}
    for block in body["view"]["state"]["values"].values():
        for setting in settings:
            if setting in block:
                data[setting] = block[setting]["value"]

    update_user_settings(body["user"]["id"], data)


if __name__ == "__main__":
    env.mongo_client.admin.command("ping")
    print("Connected to MongoDB")
    update_status()
    print(f"App is running on port {env.port}")
    app.start(port=env.port)
