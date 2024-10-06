def generate_home_view(
    lastfm_username: str | None,
    lastfm_api_key: str | None,
    steam_id: str | None,
    steam_api_key: str | None,
) -> dict:
    if (
        lastfm_api_key is None
        or lastfm_username is None
        or steam_id is None
        or steam_api_key is None
    ):
        return {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Welcome to Slick Stats",
                        "emoji": True,
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Hi there! I'll be updating your status when you use one of the various services I support. To get started, please click the button below to authorise me to update your status!",
                        "emoji": True,
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": ":slack: Authorise",
                                "emoji": True,
                            },
                            "style": "primary",
                            "url": "https://slickstats.dillonb07.studio/slack/install",
                        }
                    ],
                },
            ],
        }
    return {
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
            {"type": "divider"},
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "steam_id",
                    "initial_value": steam_id if steam_id else "",
                },
                "label": {"type": "plain_text", "text": "Steam ID", "emoji": False},
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "steam_api_key",
                    "initial_value": steam_api_key if steam_api_key else "",
                },
                "label": {
                    "type": "plain_text",
                    "text": "Steam API Key",
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