import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class YoutubeApi:

    test = 'je suis un test'
    api_service_name = 'youtube'

    def __init__(self):
        print('Je suis __init__')
        self.build = self.authenticate_youtube()

    # Authentication to API && credentials management
    def authenticate_youtube(self):
        print('je suis authenticate_youtube')
        api_service_name = "youtube"
        api_version = "v3"
        credentials = None
        if os.path.exists("credentials/token.pickle"):
            with open("credentials/token.pickle", "rb") as token:
                credentials = pickle.load(token)

        # if there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/client_secrets.json',
                    scopes=['https://www.googleapis.com/auth/youtube.readonly']
                )
                flow.run_local_server()
                credentials = flow.credentials
            # save the credentials for the next run
            with open("credentials/token.pickle", "wb") as token:
                pickle.dump(credentials, token)

        youtube = build(api_service_name, api_version, credentials=credentials)
        return youtube


    def get_playlists(self):
        request = self.build.playlists().list(
            part="snippet, contentDetails",
            mine="true",
            maxResults=50,
        )
        resp = request.execute()  # Query execution
        return resp


