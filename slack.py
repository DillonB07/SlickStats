from slack_bolt import App
import os
from db import db_client

from slack_bolt.oauth.oauth_settings import OAuthSettings

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    oauth_settings=OAuthSettings(
        client_id=os.environ.get("SLACK_CLIENT_ID"),
        client_secret=os.environ.get("SLACK_CLIENT_SECRET"),
        scopes=["chat:write", "im:history", "users.profile:read"],
        user_scopes=["users.profile:write", "users.profile:read"],
        redirect_uri=os.environ.get("SLACK_REDIRECT_URI"),
        install_path="/slack/install",
        installation_store=db_client,
        redirect_uri_path="/slack/oauth_redirect",
    ),
)


EMOJIS = {"music": ":musical_note:"}

USER_ID = "U054VC2KM9P"
current_pfp = "normal"


def update_status(emoji, status, user_token, expiry=0):
    current_status = app.client.users_profile_get(user=USER_ID, token=user_token)
    if current_status.get("ok"):
        status_emoji = current_status["profile"].get("status_emoji", ":ghost:")
    else:
        status_emoji = ":ghost:"

    if status_emoji in list(EMOJIS.values()) or status_emoji == ":ghost:":
        app.client.users_profile_set(
            profile={
                "status_text": status,
                "status_emoji": EMOJIS.get(emoji, ""),
                "status_expiration": expiry,
            },
            token=user_token,
        )


def update_pfp(type, user_token):
    global current_pfp
    path = f"pfps/{type}.png"
    if type != current_pfp:
        current_pfp = type

        app.client.users_setPhoto(token=user_token, image=open(path, "rb"))
