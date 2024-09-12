from dotenv import load_dotenv
from flask import Flask, request, redirect, session
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk.oauth.installation_store import Installation
from db import db_client
from slack import app as bolt_app
import os

load_dotenv()
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)

handler = SlackRequestHandler(bolt_app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def slack_oauth_redirect():
    code = request.args.get("code")
    client_id = os.environ.get("SLACK_CLIENT_ID", "")
    client_secret = os.environ.get("SLACK_CLIENT_SECRET", "")
    redirect_uri = os.environ.get("SLACK_REDIRECT_URI")

    response = bolt_app.client.oauth_v2_access(
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        redirect_uri=redirect_uri,
    )

    if response.get("ok"):
        installation = Installation(
            team_id=response["team"]["id"],
            user_id=response["authed_user"]["id"],
            user_token=response["authed_user"]["access_token"],
            bot_token=response["access_token"],
        )
        db_client.save(installation)
        return "Installation successful!"
    else:
        return "Installation failed!"


@flask_app.route("/slack/install", methods=["GET"])
def slack_install():
    client_id = os.environ.get("SLACK_CLIENT_ID")
    scope = "commands,chat:write,im:history,users.profile:read"
    user_scope = "users.profile:write,users.profile:read"
    redirect_uri = os.environ.get("SLACK_REDIRECT_URI")
    return redirect(
        f"https://slack.com/oauth/v2/authorize?client_id={client_id}&scope={scope}&user_scope={user_scope}&redirect_uri={redirect_uri}"
    )
