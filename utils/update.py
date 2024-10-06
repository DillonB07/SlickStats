import threading
from utils.db import get_all_users
from utils.slack import update_slack_pfp, update_slack_status, STATUSES, log_to_slack
from utils.env import env


def update_status():
    threading.Timer(25, update_status).start()
    set = False
    users = get_all_users()

    for user in list(users):
        installation = env.installation_store.find_installation(
            user_id=user.get("user_id")
        )
        if not installation:
            print("No installation found for user", user.get("user_id"))
            continue
        bot_token = installation.bot_token
        user_token = installation.user_token
        user_id = user.get("user_id")
        current_pfp = user.get("pfp")
        for status in STATUSES:
            custom, log_message = status.get(
                "function",
                lambda _: print(
                    f'Failed to run status fetching function for {status.get("name")}'
                ),
            )(user)
            if log_message:
                log_to_slack(log_message, bot_token)

            if custom:
                update_slack_status(
                    status.get("emoji"),
                    status.get("status", "").replace("(custom)", custom),
                    user_id=user_id,
                    token=user_token,
                )
                update_slack_pfp(
                    type=status.get("pfp"),
                    current_pfp=current_pfp,
                    user_id=user_id,
                    token=user_token,
                )
                set = True
                break

        if not set:
            update_slack_status(emoji="", status="", user_id=user_id, token=user_token)
            update_slack_pfp(
                type="normal",
                current_pfp=current_pfp,
                user_id=user_id,
                token=user_token,
            )
