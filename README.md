# oauth-youtube-live-stream-python
Python script that will oauth google and start live stream in youtube. It uses `FFmpeg` for video RMTP streaming and processing.

## Get Google Oauth credential
1. Got to google cloud and enable `YouTube Data API v3`
2. Click manage and generate Oauth Client ID credential, download and save the `credentials.json` in root directory
3. Make sure you register your app in the Oauth consent screen

## How to execute?
- Run `pip install -r requirements.txt`
- Add HSL stream url in `video_url` variable
- Execute `python oauth_stream_youtube.py`

## Or, Integrate as Frontend/Backend
Call this url endpoint from Frotend to intitize Oauth request
`https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=YOUR_GOOGLE_CLIENT_ID&redirect_uri=YOUR_BACKEND_REDIRECT_API&scope=YOUR_REQUIRED_PERMISSIONS&state=YOUR_STATE_CHARACTERS&access_type=offline`

Create backend redirect_endpoint and execure [this code](https://github.com/hbvj99/oauth-youtube-live-stream-python/blob/main/exchange_code_to_credential.py) to exchange code to accomplish other tasks

## License
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
