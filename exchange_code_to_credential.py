from google_auth_oauthlib.flow import InstalledAppFlow
import google.oauth2.credentials

google_client_secret_json = {
    "web": {
        "client_id": 'YOUR_GOOGLE_OAUTH_CLIENT_ID'),
        "project_id": 'YOUR_GOOGLE_OAUTH_PROJECT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": 'YOUR_GOOGLE_OAUTH_CLIENT_SECRET'),
        "redirect_uris": 'YOUR_GOOGLE_OAUTH_REDIRECT_URL')
    }}

def oauth_google_exchange_code_save_credential(code, state):
  try:
    flow = InstalledAppFlow.from_client_config(
        google_client_secret_json,
        scopes=config('GOOGLE_OAUTH_SCOPE', cast=Csv()),
        redirect_uri=config('GOOGLE_OAUTH_REDIRECT_URL', cast=Csv())[0]
    )
    credentials = flow.fetch_token(code=code)
    
    credential = google.oauth2.credentials.Credentials(
        credentials.get('access_token'),
        refresh_token=credentials.get('refresh_token'),
        token_uri='https://accounts.google.com/o/oauth2/token',
        client_id=config('GOOGLE_OAUTH_CLIENT_ID'),
        client_secret=config('GOOGLE_OAUTH_CLIENT_SECRET')
    )
    
    decoded_state = base64.b64decode(state.encode('utf-8')).decode('utf-8')
    return credentials, decoded_state
  except Exception as e:
    return 'code_invalid', False
