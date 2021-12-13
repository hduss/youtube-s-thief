# API client library
import os
import pickle
import json
import time

import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def get_credentials():
    # API information
    # API_KEY = "AIzaSyAYheEHWuVrMYXn4C4JKSv3OKMGUku73a4"
    api_service_name = "youtube"
    api_version = "v3"
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # if there are no (valid) credentials availablle, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=['https://www.googleapis.com/auth/youtube.readonly']
            )
            flow.run_local_server()
            credentials = flow.credentials
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    # Display credentials
    # print(credentials.to_json())

    youtube = build(api_service_name, api_version, credentials=credentials)
    return youtube


def get_videos(build):
    
    request = build.videos().list(
        part='contentDetails, snippet',
        myRating='like',
        maxResults=10
    )
    
    resp = request.execute()  # Query execution
    return resp


def main():
    
    build = get_credentials()  # get credentials
    response = get_videos(build)  # get videos
    
    # print(json.dumps(response, indent=2))  # Print results
    for item in response['items']:
        time.sleep(0.02)
        print("[+] " + item['snippet']['title'] + " - " + item['id'])


if __name__ == "__main__":
    main()
