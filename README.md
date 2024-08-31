# Slick Stats

I've not yet implemented OAuth so if you wish to use this app, you need to host it yourself.
Slick Stats is a Slack bot that will automatically update your Slack status to show what you're up to on a variety of platforms

## Features

- LastFM Status
- Steam Status (Coming soon™️) - *this was implemented but it broke stuff so I reverted it*



## Setup

Make a Slack app with the following manifest (make sure to switch out the URLs to yours)

```
{
    "display_information": {
        "name": "Slick Stats",
        "description": "Update your status to show what you're doing across other services!",
        "background_color": "#5c235c",
        "long_description": "Slick Stats automatically updates your status to show what you're doing on other services throughout a variety of APIs.\r\n\r\nCurrently supported:\r\n- Last.fm - `{song} - {artist}`\r\n\r\nComing soon:\r\n- Steam\r\n\r\nGot a request? Submit an issue at https://github.com/DillonB07/SlickStats!"
    },
    "features": {
        "app_home": {
            "home_tab_enabled": true,
            "messages_tab_enabled": false,
            "messages_tab_read_only_enabled": false
        },
        "bot_user": {
            "display_name": "Slick Stats",
            "always_online": true
        }
    },
    "oauth_config": {
        "scopes": {
            "user": [
                "users.profile:write"
            ],
            "bot": [
                "chat:write",
                "im:history",
                "users.profile:read"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "request_url": "https://slickstats.dillonb07.studio/slack/events",
            "bot_events": [
                "app_home_opened",
                "message.im"
            ]
        },
        "interactivity": {
            "is_enabled": true,
            "request_url": "https://slickstats.dillonb07.studio/slack/events"
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "token_rotation_enabled": false
    }
}
```

After cloning the repo:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python3.12 -m pip install -r requirements.txt
python3.12 app.py
```

You will also need the following in a `.env` file:

```
SLACK_USER_TOKEN=""
SLACK_BOT_TOKEN=""
SLACK_SIGNING_SECRET=""

MONGO_USER=""
MONGO_PASSWORD=""
MONGO_URI=""
```
