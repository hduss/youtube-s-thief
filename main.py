# API client library
import os
import pickle
import time
import json
import title
import colorama
import csv
import google.oauth2.credentials
from pytube import YouTube
from tqdm import tqdm
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

colorama.init()


# Return build of API if authenticate OK
# Create or refresh credentials
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


def get_playlists(build, channel_id):
    request = build.playlists().list(
        part="snippet",
        mine="true",
        maxResults=50

    )
    resp = request.execute()  # Query execution
    return resp


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
    resp = request.execute()
    return resp


def write_in_folder(file, song_list):
    with open(file, "w", encoding="utf-8") as f:
        for song in tqdm(song_list, desc="Writing song"):
            f.write(song + "\n")


def main():
    title.display_informations()
    nbr_pages = title.start_program()
    song_list = []
    build = authenticate_youtube()  # get credentials


    # channel_id = build['']
    playlists = get_playlists(build, "UCS08XVYyOCxYvZNtovqdaAQ")
    # print(json.dumps(playlists, indent=2))

    url = "https://www.youtube.com/watch?v=m8j56gQHICw&list=LL&index=6&ab_channel=Laylow-Topic"
    yt = YouTube(url)
    print(yt.title)
    print(yt.streams)
    print(yt.streams.filter(only_audio=True).all)
    stream = yt.streams.get_by_itag(139)
    stream.download('downloads')

    print('list of playlists find : ')

    id_uploads = "UUS08XVYyOCxYvZNtovqdaAQ"

    # list of title's playlists
    for items in playlists['items']:
        print(json.dumps(items['snippet']['localized']['title'], indent=2))

    if nbr_pages > 0:

        response = get_videos(build)  # get videos
        next_page_token = response['nextPageToken']

        print(colorama.Fore.GREEN + colorama.Style.NORMAL)
        # print(json.dumps(response, indent=2))  # Print results
        for item in tqdm(response['items'], desc="Processing page 1"):
            song = item['snippet']['title'] + " --- " + item['id']
            song_list.append(song)

            # print(song_liste)
            # print(colorama.Fore.YELLOW + colorama.Style.NORMAL + "[+] " + item['snippet']['title'] + " --- " + item[
            #     'id'] + colorama.Style.RESET_ALL)

        i = 1  # For DEBUG

        # While loop for next page | get_video_next_page() function
        while next_page_token and i < nbr_pages:

            r = get_video_next_page(build, next_page_token)
            next_page_token = r['nextPageToken']
            # print("Next Page Token while => " + next_page_token)
            for item in tqdm(r['items'], desc="Processing page " + str(i + 1)):
                song = item['snippet']['title'] + " --- " + item['id']
                song_list.append(song)

                # print(colorama.Fore.YELLOW + colorama.Style.NORMAL + "[+] " + item['snippet']['title'] + " --- " +
                # item[ 'id'] + colorama.Style.RESET_ALL)

            i += 1  # For DEBUG

        write_in_folder('uploads/song.txt', song_list)

    else:
        print('Aucune vidéo n\' été téléchargé')


if __name__ == "__main__":
    main()
