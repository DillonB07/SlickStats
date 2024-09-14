import threading

import requests
import json

BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_playing(api_key: str, username: str) -> dict:
    url = f"{BASE_URL}?method=user.getrecenttracks&api_key={api_key}&format=json&user={username}"
    response = requests.get(url)
    return response.json()


def get_lastfm_status(user) -> str | None:
    api_key = user.get("lastfm_api_key")
    username = user.get("lastfm_username")
    if not api_key or not username:
        return

    playing = get_playing(api_key, username)
    current = playing.get("recenttracks", {}).get("track")[0]
    if current.get("@attr") and current.get("@attr").get("nowplaying"):
        return f"{current.get('name')} - {current.get('artist')['#text']}"
    else:
        return None
