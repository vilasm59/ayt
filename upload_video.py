import os
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# YouTube API credentials from GitHub Secrets
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Authenticate using the refresh token
credentials = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

youtube = build("youtube", "v3", credentials=credentials)

# Video details
video_file = "श्री हनुमान चालीसा Hanuman Chalisa I GULSHAN KUMAR I HARIHARAN, Full.mp4"  # Replace with your actual video file name
request_body = {
    "snippet": {
        "title": "श्री हनुमान चालीसा 1 Hour loop Series | Shree Hanuman Chalisa Video",
        "categoryId": "24"  # Category 22 = People & Blogs
    },
    "status": {
        "privacyStatus": "public",  # Options: 'public', 'unlisted', 'private'
    }
}

# Upload the video
media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
response = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media).execute()

print(f"✅ Video uploaded! Watch here: https://www.youtube.com/watch?v={response['id']}")
