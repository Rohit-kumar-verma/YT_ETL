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
            print(video_ids[0])
            return video_ids

        except requests.exceptions.RequestException as e:
            raise e


def extract_video_data(video_ids, batch_size):
    video_details = []
    for i in range(0, len(video_ids), batch_size):
        batch_ids = video_ids[i:i + batch_size]
        
        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={','.join(batch_ids)}&key={api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            for item in data.get("items", []):
                video_id= item["id"]
                title = item["snippet"]["title"]
                duration = item["contentDetails"]["duration"]
                published_at = item["snippet"]["publishedAt"]
                view_count = item["statistics"].get("viewCount", None)
                like_count = item["statistics"].get("likeCount", None)
                comment_count = item["statistics"].get("commentCount", None)
                video_details.append({
                    "video_id": video_id,
                    "title": title,
                    "duration": duration,
                    "publishedAt": published_at,
                    "view_count": view_count,
                    "like_count": like_count,
                    "comment_count": comment_count
                })
        except requests.exceptions.RequestException as e:
            raise e
    return video_details

if __name__ == "__main__":
    Channel_playlistId = get_video_stats(Channel_handle)
    video_ids = get_videoIds(Channel_playlistId)
    extract_video_data(video_ids, batch_size=50)