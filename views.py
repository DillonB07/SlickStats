def generate_home_view(lastfm_username: str, lastfm_api_key: str, steam_id: str, steam_api_key: str) -> dict:
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "SlickStats Settings",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "lastfm_username",
                    "initial_value": lastfm_username if lastfm_username else ""
                },
                "label": {
                    "type": "plain_text",
                    "text": "Last.fm Username",
                    "emoji": False
                }
            },{
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "lastfm_api_key",
                    "initial_value": lastfm_api_key if lastfm_api_key else ""
                },
                "label": {
                    "type": "plain_text",
                    "text": "Last.fm API Key",
                    "emoji": False
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "steam_id",
                    "initial_value": steam_id if steam_id else ""
                },
                "label": {
                    "type": "plain_text",
                    "text": "Steam ID",
                    "emoji": False
                }
            },{
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "steam_api_key",
                    "initial_value": steam_api_key if steam_api_key else ""
                },
                "label": {
                    "type": "plain_text",
                    "text": "Steam API Key",
                    "emoji": False
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Submit",
                            "emoji": True
                        },
                        "value": "submit_settings",
                        "action_id": "submit_settings"
                    }
                ]
            }
        ]
    }
