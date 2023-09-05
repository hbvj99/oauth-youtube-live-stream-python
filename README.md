# oauth-youtube-live-stream-python
Python script that will oauth google and start live stream in youtube

## Get Google Oauth credential
1. Got to google cloud and enable `YouTube Data API v3`
2. Click manage and generate Oauth Client ID credential, download and save the `credentials.json` in root directory
3. Make sure you register your app in the Oauth consent screen

## How to execute?
- Run `pip install -r requirements.txt`
- Add HSL stream url in `video_url` variable
- Execute `python oauth_stream_youtube.py`
