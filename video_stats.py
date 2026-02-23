import requests
import json
from datetime import date
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
        
        Channel_items= data["items"][0]
        related_playlists = Channel_items["contentDetails"]["relatedPlaylists"]
        Channel_playlistID = related_playlists["uploads"]
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


def save_to_json(extracted_data):
    filepath = f"./data/YT_data_{date.today()}.json"

    with open(filepath, 'w', encoding='utf-8') as json_output:
        json.dump(extracted_data, json_output, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    Channel_playlistId = get_video_stats(Channel_handle)
    video_ids = get_videoIds(Channel_playlistId)
    video_data = extract_video_data(video_ids, batch_size=50)
    save_to_json(video_data)