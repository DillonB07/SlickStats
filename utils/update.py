import threading
from utils.db import db_client
from utils.slack import update_slack_pfp, update_slack_status, STATUSES, log_to_slack
from utils.env import env

import os


def update_status():
    threading.Timer(25, update_status).start()
    set = False
    users = db_client.users.find()
    for user in users:
        token = user.get("user_token")
        user_id = user.get("user_id")
        for status in STATUSES:
            custom, log_message = status.get(
                "function",
                lambda _: print(
                    'Failed to run status fetching function for {status.get("name")}'
                ),
            )(user)
            if log_message:
                log_to_slack(log_message)

            if custom:
                update_slack_status(
                    status.get("emoji"),
                    status.get("status", "").replace("(custom)", custom),
                    user_id=user_id,
                    token=token,
                )
                update_slack_pfp(type=status.get("pfp"), user_id=user_id, token=token)
                set = True
                break

        if not set:
            update_slack_status(emoji="", status="", user_id=user_id, token=token)
            update_slack_pfp(type="normal", user_id=user_id, token=token)
