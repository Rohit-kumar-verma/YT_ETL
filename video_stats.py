import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')  # Load environment variables from .env file

api_key = os.getenv("api_key")
Channel_handle = "MrBeast"

def get_video_stats(Channel_handle):
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

def get_videoIds(Channel_playlistId):
        video_ids = []
        pageToken = None
        baseUrl = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&&maxResults=50&playlistId={Channel_playlistId}&key={api_key}"
        
        try:
            while True:
                url = baseUrl
                if pageToken:
                    url += f"&pageToken={pageToken}"
                 
                response = requests.get(url)
                data = response.json()
                video_items = data["items"]
                video_ids.extend([item["contentDetails"]["videoId"] for item in video_items])
                pageToken = data.get("nextPageToken")
                if not pageToken:
                    break

            return video_ids

        except requests.exceptions.RequestException as e:
            raise e

if __name__ == "__main__":
    Channel_playlistId = get_video_stats(Channel_handle)
    get_videoIds(Channel_playlistId)