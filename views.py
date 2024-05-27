HOME = {
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
                "action_id": "lastfm_username"
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
                "action_id": "lastfm_api_key"
            },
            "label": {
                "type": "plain_text",
                "text": "Last.fm API Key",
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