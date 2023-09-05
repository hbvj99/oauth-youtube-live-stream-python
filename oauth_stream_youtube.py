import datetime
import os
import pickle
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

"""
package to install google-auth-oauthlib, google-api-python-client
"""


def are_credentials_expired(credentials):
    if isinstance(credentials, Credentials):
        return credentials.expiry < datetime.datetime.utcnow()
    return True


def save_credentials(credentials, filename):
    with open(filename, 'wb') as token_file:
        pickle.dump(credentials, token_file)


def load_credentials(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as token_file:
            return pickle.load(token_file)
    return None


def oauth_google():
    credentials_filename = "my_credentials.pickle"
    credentials = load_credentials(credentials_filename)
    if not credentials or are_credentials_expired(credentials):
        # credentials.json should be in same directory
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", scopes=["https://www.googleapis.com/auth/youtube"])

        credentials = flow.run_local_server()
        save_credentials(credentials, credentials_filename)

    # Create a YouTube Data API service instance
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def live_stream_video_to_youtube(ingest_url, video_url, stream_key):
    ffmpeg_command = [
        "ffmpeg",
        "-i", video_url,
        "-r", "30",
        "-c:v", "copy",
        "-b:v", "4500k",
        "-c:a", "aac",
        "-strict", "experimental",
        "-f", "flv",
        f"{ingest_url}/{stream_key}"
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)


def start_live_stream(event_id):
    try:
        # Transition the live stream to "live" status
        request = youtube.liveBroadcasts().transition(
            part="id,snippet",
            id=event_id,
            broadcastStatus="live"
        )
        response = request.execute()
        print("Live stream started:", response)
    except Exception as e:
        print("An error occurred while starting the live stream:", e)


def create_live_stream(title):
    try:
        # Create a live stream
        stream_request = youtube.liveStreams().insert(
            part="snippet,cdn",
            body={
                "kind": "youtube#liveStream",
                "snippet": {
                    "title": title,
                },
                "cdn": {
                    "ingestionType": "rtmp",
                    "resolution": "1080p",
                    "frameRate": "30fps",
                }
            }
        )
        stream_response = stream_request.execute()
        print("Live stream created:", stream_response)
        return stream_response

    except Exception as e:
        print("An error occurred while creating live stream:", e)
        return None


def create_live_event(title, description, start_time, end_time):
    try:
        # Create a live broadcast
        broadcast_request = youtube.liveBroadcasts().insert(
            part="snippet,status,contentDetails",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "scheduledStartTime": start_time,
                    "scheduledEndTime": end_time,
                },
                "status": {
                    "privacyStatus": "private",  # private, public, unlisted
                    "selfDeclaredMadeForKids": False
                },
                "contentDetails": {
                    "enableAutoStart": True,
                    "enableAutoStop": True,
                    "latencyPreference": "ultraLow"

                }
            }
        )
        broadcast_response = broadcast_request.execute()
        print("Live event created:", broadcast_response)
        return broadcast_response

    except Exception as e:
        print("An error occurred while creating live event:", e)
        return None


def bind_live_stream_to_event(event_id, live_stream_id):
    try:
        # Bind the live stream to the live broadcast
        bind_request = youtube.liveBroadcasts().bind(
            part="id,contentDetails",
            id=event_id,
            streamId=live_stream_id
        )
        bind_response = bind_request.execute()
        print("Stream bound to event:", bind_response)

    except Exception as e:
        print("An error occurred while binding stream to event:", e)


if __name__ == "__main__":
    youtube = oauth_google()

    event_title = "Summer day 17"
    event_description = "Description of my live event"
    start_time = datetime.datetime.utcnow().isoformat() + "Z"  # Start time in ISO 8601 format
    end_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + "Z"  # End time

    schedule_event = create_live_event(event_title, event_description, start_time, end_time)

    if schedule_event:
        live_stream = create_live_stream(event_title)
        live_stream_id = live_stream["id"]
        stream_key = live_stream["cdn"]["ingestionInfo"]["streamName"]
        ingest_url = live_stream["cdn"]["ingestionInfo"]["ingestionAddress"]

        event_id = schedule_event["id"]

        print("Live event broadcast ID:", event_id)
        print("Live stream ID:", live_stream_id)
        print("Stream key:", stream_key)

        bind_live_stream_to_event(event_id, live_stream_id)
        start_live_stream(event_id)

        video_url = "https://YOUR_HLS_STREAM_URL.m3u8"
        live_stream_video_to_youtube(ingest_url, video_url, stream_key)
