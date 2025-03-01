import os
import google.auth.transport.requests
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials
import requests

# Load environment variables
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Function to refresh access token
def get_access_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to refresh access token")

# Function to upload a video
def upload_video(video_file, title="Daily Upload", description="Automated upload", category_id="22", privacy_status="public"):
    access_token = get_access_token()
    
    credentials = google.oauth2.credentials.Credentials(access_token)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["automation", "daily upload"],
            "categoryId": category_id,
        },
        "status": {"privacyStatus": privacy_status},
    }
    
    with open(video_file, "rb") as file:
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=googleapiclient.http.MediaIoBaseUpload(file, mimetype="video/mp4", chunksize=-1, resumable=True),
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
        
    print("Upload complete!")
    return response

if __name__ == "__main__":
    video_path = "video.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found!")
        exit(1)
    
    upload_video(video_path)
