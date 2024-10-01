import threading
from db import get_user_settings
from slack import update_slack_pfp, update_slack_status, STATUSES, log_to_slack

import os

def update_status():
    threading.Timer(25, update_status).start()
    set = False
    user = get_user_settings(os.environ.get("SLACK_USER_ID"))
    for status in STATUSES:
        custom, log_message = status.get("function", lambda _: print('Failed to run status fetching function for {status.get("name")}'))(user)
        if log_message:
            log_to_slack(log_message)

        if custom:
            # print(f"Setting pfp and status for {status.get("name")} to {status.get("status","").replace("(custom)", custom)} with {status.get("pfp")} pfp.")
            update_slack_status(status.get("emoji"), status.get("status","").replace("(custom)", custom), os.environ.get("SLACK_USER_ID"))
            update_slack_pfp(status.get("pfp"))
            set = True
            break

    if not set:
        update_slack_status("", "", os.environ.get("SLACK_USER_ID"))
        update_slack_pfp("normal")
