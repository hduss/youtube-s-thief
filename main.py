# API client library
import youtubeList.title as title
import os
import pickle
import requests
import time
import json
import colorama
import csv
import argparse
import google.oauth2.credentials
from pytube import YouTube
from tqdm import tqdm
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Colorama init and variables
colorama.init()
colorama_plus = '[' + colorama.Fore.GREEN + '+' + colorama.Style.RESET_ALL + ']'
colorama_less = '[' + colorama.Fore.RED + '-' + colorama.Style.RESET_ALL + ']'
colorama_yellow = colorama.Fore.YELLOW
colorama_end = colorama.Style.RESET_ALL


# @todo: Need change color arg
def colorama_color_variable(text, color):
    # return colorama.Fore.color.upper() + text + colorama.Style.RESET_ALL
    print('colorama_color')


# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', help='Show all your youtube playlists to save them',
                    action='store_true')
# parser.add_argument("-v", "--verbose", help="increase output verbosity",
#                     action="store_true")
parser.add_argument('-r', '--registered', help='List your locally saved playlists to then download the videos',
                    action="store_true")
parser.add_argument('-t', '--traduct', help='Show all your youtube playlists to save them')
parser.add_argument('--download', help='Download a playlist/video from his ID or from url')

args = parser.parse_args()


# print(args)


# Return build of API if authenticate OK
# Create or refresh credentials
def authenticate_youtube():
    api_service_name = "youtube"
    api_version = "v3"
    credentials = None
    if os.path.exists("credentials/token.pickle"):
        with open("credentials/token.pickle", "rb") as token:
            credentials = pickle.load(token)

    # if there are no (valid) credentials availablle, let the user log in.
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


def get_playlists(build):
    request = build.playlists().list(
        part="snippet",
        mine="true",
        maxResults=50
    )
    resp = request.execute()  # Query execution
    return resp


# playlist_id : 'LL' is for liked videos
def get_playlists_items(build, playlist_id):
    request = build.playlistItems().list(
        part='contentDetails, snippet',
        playlistId=playlist_id,
        maxResults=50
    )
    resp = request.execute()  # Query execution
    return resp


def get_liked_videos(build):
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


# def download_playlist():
#     url = "https://www.youtube.com/watch?v=m8j56gQHICw&list=LL&index=6&ab_channel=Laylow-Topic"
#     yt = YouTube(url)
#     print(yt.title)
#     print(yt.streams)
#     print(yt.streams.filter(only_audio=True).all)
#     stream = yt.streams.get_by_itag(139)
#     stream.download('downloads')


def search_existing_registered_playlist(playlist_name):
    return os.path.isfile('uploads/' + playlist_name + '.txt')


def compare_nbr_items_playlists():
    print('compare')


def main():
    nbr_pages = 0
    song_list = []

    title.start_program()
    # nbr_pages = title.start_program()
    # Input if not authenticate on youtube
    # auth_yt = input('You need to authenticate from youtube (Y/N) : ')

    build = authenticate_youtube()  # get credentials

    if args.list:

        playlist_dictionary = {}
        playlists = get_playlists(build)
        # Add liked videos in dictionary at 1st key
        playlist_dictionary[1] = {'title': 'Liked videos', 'id': 'LL',
                                  'registered': search_existing_registered_playlist('Liked videos')}

        for ids, items in enumerate(playlists['items'], start=2):
            playlist_title = items['snippet']['localized']['title']
            playlist_dictionary[ids] = {
                'title': playlist_title,
                'id': items['id'],
                'registered': search_existing_registered_playlist(playlist_title)
            }
        # print(json.dumps(playlist_dico_2, indent=2))
        while True:

            print('List of playlists found from your account :')
            print()

            for key, value in playlist_dictionary.items():
                registered = colorama.Fore.RED + ' (Playlist no registered localy) ' + colorama.Style.RESET_ALL
                if value['registered']:
                    registered = colorama.Fore.GREEN + ' (Playlist allready registered localy) ' + colorama.Style.RESET_ALL

                print(colorama_plus, key, '-', value['title'] + registered)

            print(colorama_yellow)
            consent = input('Do you want download a playlist locally ? (Y/N) ')

            if consent == 'Y' or consent == 'y':

                playlist_id = input('Choose playlist by ID : ')
                print(colorama.Style.RESET_ALL)

                if 1 <= int(playlist_id) < len(playlist_dictionary):

                    print(colorama_plus, 'Playlist choose : ', playlist_dictionary[int(playlist_id)]['title'])
                    playlist_items = get_playlists_items(build, playlist_dictionary[int(playlist_id)]['id'])
                    # print(json.dumps(playlist_items, indent=2))

                    for item in playlist_items['items']:
                        song = item['snippet']['title'] + " --- " + item['id']
                        song_list.append(song)

                    write_in_folder('uploads/' + playlist_dictionary[int(playlist_id)]['title'] + '.txt', song_list)

                    # CLear and MAJ datas for while loop
                    song_list.clear()
                    if search_existing_registered_playlist(playlist_dictionary[int(playlist_id)]['title']):
                        playlist_dictionary[int(playlist_id)]['registered'] = True
                else:
                    print(colorama_less + colorama.Fore.RED + ' Error : Value ' + playlist_id + ' is not valid' +
                          colorama_end)
                    print()

            else:
                print('End of program ...')
                return

    elif args.registered:

        print(os.listdir("uploads"))

    elif args.download:
        print('je suis DL')
        print(args.download)
        r = requests.get(args.download)
        print(r)

    elif args.traduct:
        print(args.traduct)

    else:
        print('No playlists found')

    # channel_id = build['']

    # print(json.dumps(playlists, indent=2))

    id_uploads = "UUS08XVYyOCxYvZNtovqdaAQ"

    if nbr_pages > 0:

        response = get_liked_videos(build)  # get videos
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

        write_in_folder('uploads/Liked videos.txt', song_list)

    else:
        print('No videos downloaded')


if __name__ == "__main__":
    main()
