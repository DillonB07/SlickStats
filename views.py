from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from db import db_client
import os

load_dotenv()
# slack_client = WebClient(os.getenv("SLACK_BOT_TOKEN"))

def generate_home_view(user_id: str, client):
    # check if the user is authed
    user = db_client.find_user(user_id=user_id)
    if not user:
        user = {}
        view = {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "SlickStats",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Welcome to SlickStats! To get started, please [authorize the app](https://slack.com/oauth/v2/authorize?client_id=CLIENT_ID&scope=commands,chat:write,im:write,users.profile:read&user_scope=users.profile:read&redirect_uri=REDIRECT_URI) first.",
                    },
                },
            ],
        }
    elif not user.get("bot_token") or not user.get("user_token"):
        view = {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "SlickStats",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Authorization failed. Please try again.",
                    },
                },
            ],
        }
    else:
        lastfm_username = user.get("lastfm_username")
        lastfm_api_key = user.get("lastfm_api_key")

        view = {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "SlickStats Settings",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "lastfm_username",
                        "initial_value": lastfm_username if lastfm_username else "",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Last.fm Username",
                        "emoji": False,
                    },
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "lastfm_api_key",
                        "initial_value": lastfm_api_key if lastfm_api_key else "",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Last.fm API Key",
                        "emoji": False,
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Submit", "emoji": True},
                            "value": "submit_settings",
                            "action_id": "submit_settings",
                        }
                    ],
                },
            ],
        }

    try:
        client.views_publish(user_id=user_id, view=view, token=user.get("bot_token", os.getenv("SLACK_BOT_TOKEN")))
    except SlackApiError as e:
        print(f"Error publishing home view: {e.response['error']}")
