from slack_bolt import App
from status.lastfm import get_lastfm_status
from status.steam import get_steam_status

import os

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
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
app.user_token = os.environ.get("SLACK_USER_TOKEN")

current_pfp = "normal"


def update_slack_status(emoji, status, user_id, expiry=0):
    current_status = app.client.users_profile_get(user=user_id)
    if current_status.get("ok"):
        status_emoji = current_status["profile"].get("status_emoji", "")
    else:
        status_emoji = ""

    emojis = [e.get("emoji") for e in STATUSES]

    if status_emoji in emojis or status_emoji == "":
        app.client.users_profile_set(
            token=app.user_token,
            profile={
                "status_text": status,
                "status_emoji": emoji,
                "status_expiration": expiry,
            },
        )


def update_slack_pfp(type):
    global current_pfp
    path = f"pfps/{type}.png"
    if type != current_pfp:
        current_pfp = type
        app.client.users_setPhoto(token=app.user_token, image=open(path, "rb"))
    return


def log_to_slack(message):
    app.client.chat_postMessage(
        channel=os.environ.get("SLACK_LOG_CHANNEL"), text=message
    )
