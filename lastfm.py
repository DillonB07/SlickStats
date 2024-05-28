import threading

import requests
import json

from slack import update_status

BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_playing(api_key: str, username: str) -> dict:
    url = f"{BASE_URL}?method=user.getrecenttracks&api_key={api_key}&format=json&user={username}"
    response = requests.get(url)
    return response.json()


def update_lastfm_status() -> bool:
    threading.Timer(25, update_lastfm_status).start()
    with open("cache.json", "r") as f:
        data = json.load(f)
    for user in data:
        api_key = user.get("lastfm_api_key")
        username = user.get("lastfm_username")
        if not api_key or not username:
            return False

        playing = get_playing(api_key, username)
        current = playing.get("recenttracks").get("track")[0]
        if current.get("@attr") and current.get("@attr").get("nowplaying"):
            update_status(
                ":musical_note:",
                f"{current.get('name')} - {current.get('artist')['#text']}",
            )
            return True
        else:
            update_status("", "")
            return True
