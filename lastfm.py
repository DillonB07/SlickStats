import threading

import requests
import json

from slack import update_status, update_pfp

BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_playing(api_key: str, username: str) -> dict:
    url = f"{BASE_URL}?method=user.getrecenttracks&api_key={api_key}&format=json&user={username}"
    response = requests.get(url)
    return response.json()


def update_lastfm_status():
    threading.Timer(25, update_lastfm_status).start()
    with open("cache.json", "r") as f:
        data = json.load(f)
    for user in data:
        api_key = user.get("lastfm_api_key")
        username = user.get("lastfm_username")
        user_token = user.get("user_token")
        if not api_key or not username or not user_token:
            return

        playing = get_playing(api_key, username)
        current = playing.get("recenttracks", {}).get("track")[0]
        if current.get("@attr") and current.get("@attr").get("nowplaying"):
            update_status(
                "music",
                f"{current.get('name')} - {current.get('artist')['#text']}",
                user_token,
            )
            update_pfp("music", user_token)
            return
        else:
            update_status("", "", user_token)
            update_pfp("normal", user_token)
            return True
