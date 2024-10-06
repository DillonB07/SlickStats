import requests

BASE_URL = "http://ws.audioscrobbler.com/2.0/"

current_song = ""


def get_playing(api_key: str, username: str) -> dict:
    """

    :param api_key: str:
    :param username: str:
    :param api_key: str: 
    :param username: str: 

    """
    url = f"{BASE_URL}?method=user.getrecenttracks&api_key={api_key}&format=json&user={username}"
    response = requests.get(url)
    return response.json()


def get_lastfm_status(user) -> tuple[str | None, str | None]:
    """

    :param user: 

    """
    global current_song
    api_key = user.get("lastfm_api_key")
    username = user.get("lastfm_username")
    if not api_key or not username:
        return None, None

    playing = get_playing(api_key, username)
    current = playing.get("recenttracks", {}).get("track", [])
    if not current:
        return None, None
    current = current[0]
    if current.get("@attr") and current.get("@attr").get("nowplaying"):
        new = f"{current.get('name')} - {current.get('artist')['#text']}"
        if current_song == new:
            return new, None
        else:
            current_song = new
            log_message = f"Last.fm: <https://last.fm/user/{username}|{username}> is playing {current.get('name')} by {current.get('artist')['#text']}"
            return new, log_message

    else:
        return None, None
