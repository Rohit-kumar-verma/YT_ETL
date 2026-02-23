import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')  # Load environment variables from .env file

api_key = os.getenv("api_key")
Channel_handle = "MrBeast"

def get_video_stats(Channel_handle, api_key):
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={Channel_handle}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        # print(json.dumps(data, indent=2))
        Channel_items= data["items"][0]
        related_playlists = Channel_items["contentDetails"]["relatedPlaylists"]
        Channel_playlistID = related_playlists["uploads"]
        print(f"Channel Playlist ID: {Channel_playlistID}")
        return Channel_playlistID

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    get_video_stats(Channel_handle, api_key)