import threading

import requests
import json

from slack import update_status, update_pfp

BASE_URL = "https://api.steampowered.com"


def get_playing(api_key: str, user_id: str) -> dict:
    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&format=json&steamids={user_id}"
    response = requests.get(url)
    return response.json()


def update_steam_status():
    threading.Timer(25, update_steam_status).start()
    with open("cache.json", "r") as f:
        data = json.load(f)
    for user in data:
        api_key = user.get("steam_api_key")
        user_id = user.get("steam_id")
        if not api_key or not user_id:
            return

        playing = get_playing(api_key, user_id)
        current = playing.get("response", {}).get("players", [])[0].get("gameextrainfo")
        if current:
            update_status("gaming", f"Playing {current} via Steam")
            update_pfp("gaming")
            return
        else:
            update_status("", "")
            update_pfp("normal")
            return
    return
