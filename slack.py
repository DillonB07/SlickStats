from slack_bolt import App
import os

app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get(
    "SLACK_SIGNING_SECRET"))
app.user_token = os.environ.get("SLACK_USER_TOKEN")


def update_status(emoji, status, expiry=0):
    app.client.users_profile_set(
        token=app.user_token,
        profile={
            "status_text": status,
            "status_emoji": emoji,
            "status_expiration": expiry
        }
    )

def update_pfp(type):
    path = f'pfps/{type}.png'
    app.client.users_setPhoto(
        token=app.user_token,
        image=open(path, 'rb')
    )
