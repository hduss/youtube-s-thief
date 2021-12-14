# API client library
import os
import pickle
import time
import title
import colorama
import google.oauth2.credentials
from tqdm import tqdm
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

colorama.init()


def authenticate_youtube():
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

    youtube = build(api_service_name, api_version, credentials=credentials)
    return youtube


def get_videos(build):
    request = build.videos().list(
        part='contentDetails, snippet',
        myRating='like',
        maxResults=50
    )

    resp = request.execute()  # Query execution
    return resp


def get_video_next_page(build, next_page_token):
    request = build.videos().list(
        part='contentDetails, snippet',
        myRating='like',
        maxResults=50,
        pageToken=next_page_token
    )

    resp = request.execute()  # Query execution
    return resp


def main():
    title.display_informations()
    nbr_pages = title.start_program()

    if nbr_pages > 0:
        for i in tqdm(range(50)):
            time.sleep(0.01)

        build = authenticate_youtube()  # get credentials
        response = get_videos(build)  # get videos
        next_page_token = response['nextPageToken']

        # print(json.dumps(response, indent=2))  # Print results
        for item in response['items']:
            time.sleep(0.03)

            print(colorama.Fore.YELLOW + colorama.Style.NORMAL + "[+] " + item['snippet']['title'] + " - " + item[
                'id'] + colorama.Style.RESET_ALL)

        i = 1  # For DEBUG
        # While loop for next page | get_video_next_page() function
        while next_page_token and i < nbr_pages:
            r = get_video_next_page(build, next_page_token)
            next_page_token = r['nextPageToken']
            print("Next Page Token while => " + next_page_token)
            for item in r['items']:
                time.sleep(0.03)

                print(colorama.Fore.YELLOW + colorama.Style.NORMAL + "[+] " + item['snippet']['title'] + " --- " + item[
                    'id'] + colorama.Style.RESET_ALL)

            i += 1  # For DEBUG

    else:
        print('Aucune vidéo n\' été téléchargé')


if __name__ == "__main__":
    main()
