from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings

from status.lastfm import get_lastfm_status
from status.steam import get_steam_status
from utils.db import update_user_settings
from utils.env import env

STATUSES = [
    {
        "name": "Steam",
        "emoji": ":video_game:",
        "status": "Playing (custom) via Steam",
        "pfp": "gaming",
        "function": get_steam_status,
    },
    {
        "name": "Last.fm",
        "emoji": ":musical_note:",
        "status": "(custom)",
        "pfp": "music",
        "function": get_lastfm_status,
    },
]

oauth_settings = OAuthSettings(
    client_id=env.slack_client_id,
    client_secret=env.slack_client_secret,
    installation_store=env.installation_store,
    user_scopes=["users.profile:read", "users.profile:write", "users:read"],
    scopes=["chat:write", "im:history", "users.profile:read", "commands", "team:read"],
)

app = App(signing_secret=env.slack_signing_secret, oauth_settings=oauth_settings)


def update_slack_status(emoji, status, user_id, token, expiry=0):
    current_status = app.client.users_profile_get(user=user_id, token=token)
    if current_status.get("ok"):
        status_emoji = current_status["profile"].get("status_emoji", "")
    else:
        status_emoji = ""

    emojis = [e.get("emoji") for e in STATUSES]

    if status_emoji in emojis or status_emoji == "":
        app.client.users_profile_set(
            user=user_id,
            profile={
                "status_text": status,
                "status_emoji": emoji,
                "status_expiration": expiry,
            },
            token=token,
        )


def update_slack_pfp(type, user_id, current_pfp, token):
    path = f"pfps/{type}.png"
    if type != current_pfp:
        update_user_settings(user_id, {"pfp": type})
        app.client.users_setPhoto(image=open(path, "rb"), token=token)
    return


def log_to_slack(message, token):
    app.client.chat_postMessage(
        channel=env.slack_log_channel, text=message, token=token
    )
