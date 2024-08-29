from slack_bolt import App
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get(
    "SLACK_SIGNING_SECRET"))
app.user_token = os.environ.get("SLACK_USER_TOKEN")

EMOJIS = {
    "music": ":musical_note:"
}

USER_ID = "U054VC2KM9P"
CURRENT_PFP = "normal"

def update_status(emoji, status, expiry=0):
    current_status = app.client.users_profile_get(user=USER_ID)
    if current_status.get("ok"):
        status_emoji = current_status["profile"].get("status_emoji", ":ghost:")
    else:
        status_emoji = ":ghost:"

    if status_emoji in list(EMOJIS.values()) or status_emoji == "":
        app.client.users_profile_set(
            token=app.user_token,
            profile={
                "status_text": status,
                "status_emoji": EMOJIS.get(emoji, ""),
                "status_expiration": expiry
            }
        )


def update_pfp(type):
    path = f'pfps/{type}.png'
    if type != CURRENT_PFP:
        CURRENT_PFP = type
        app.client.users_setPhoto(
            token=app.user_token,
            image=open(path, 'rb')
        )
