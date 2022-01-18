# API client library
import youtubeList.title as title
import youtubeList.settings as settings
import os
import pickle
import requests
import json
import colorama
import argparse
import youtube_dl
import google.oauth2.credentials
from pytube import Playlist, YouTube
from tqdm import tqdm
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Colorama init and variables
colorama.init()
colorama_plus = '[' + colorama.Fore.GREEN + '+' + colorama.Style.RESET_ALL + ']'
colorama_plus_yellow = '[' + colorama.Fore.YELLOW + '+' + colorama.Style.RESET_ALL + ']'
colorama_less = '[' + colorama.Fore.RED + '-' + colorama.Style.RESET_ALL + ']'
colorama_yellow = colorama.Fore.YELLOW
colorama_end = colorama.Style.RESET_ALL

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', help='Show all your youtube playlists to save them',
                    action='store_true')
parser.add_argument('-r', '--registered', help='List your locally saved playlists to then download the videos',
                    action="store_true")
parser.add_argument('-t', '--test', help='Show all your youtube playlists to save them',
                    action='store_true')
parser.add_argument('-t2', '--test2', help='Show all your youtube playlists to save them',
                    action='store_true')
parser.add_argument('-d', '--download', help='Download a playlist/video from his ID or from url',
                    nargs='?', const="download_playlist")
parser.add_argument('-c', '--cut', help='cut a video in several song')
args = parser.parse_args()
print(args)


# Return build of API if authenticate OK
# Create or refresh credentials
def authenticate_youtube():
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


# Get playlists from youtube account
def get_playlists(build):
    request = build.playlists().list(
        part="snippet",
        mine="true",
        maxResults=50
    )
    resp = request.execute()  # Query execution
    return resp


# Get all videos from a playlist by id's playlist
def get_playlists_items(build, playlist_id):
    request = build.playlistItems().list(
        part='contentDetails, snippet',
        playlistId=playlist_id,
        maxResults=50
    )
    resp = request.execute()  # Query execution
    return resp


# Get next videos from playlist if more than 50 videos
def get_playlist_items_next(build, playlist_id, next_page_token):
    request = build.playlistItems().list(
        part='contentDetails, snippet',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )
    resp = request.execute()  # Query execution
    return resp


# Get videos from liked videos playlist
def get_liked_videos(build):
    request = build.videos().list(
        part='contentDetails, snippet',
        myRating='like',
        maxResults=50
    )
    resp = request.execute()  # Query execution
    return resp


# get next page from youtube-api (if there is more than 50 videos per playlist)
def get_video_next_page(build, next_page_token):
    request = build.videos().list(
        part='contentDetails, snippet',
        myRating='like',
        maxResults=50,
        pageToken=next_page_token
    )
    resp = request.execute()
    return resp


# registered song name and yoputube id in file (/uploads)
def write_in_folder(file, song_list):
    txt_file = file.split('/')[-1]
    print(txt_file)
    with open(file, 'w', encoding='utf-8') as f:
        for song in tqdm(song_list, desc=f'Writing song in {txt_file}'):
            f.write(song + "\n")


# Downloading a playlist from .txt file
def download_playlist(filename, file_format):
    with open('uploads/' + filename, encoding="utf8") as lines:

        folder_name = filename.split('.txt')[0]
        counter_corrupt_videos = 0
        corrupted_videos = []
        stream = False
        download_folder = f'downloads/{folder_name}/{file_format}'
        print(f'download folder => {download_folder}')

        for line in lines:

            split_line = line.split('---')
            # Exemple => don't become dont in download pytube
            video_name = split_line[0].strip().replace('\'', '').replace('.', '')
            print(f'Video name is {video_name}')
            video_id = split_line[1].strip()
            url = 'https://www.youtube.com/watch?v=' + video_id

            try:
                yt = YouTube(url)
                yt.check_availability()  # test availability on url
                stream = yt.streams.filter(only_audio=True).first()  # Test for age restricted
            except:
                corrupted_videos.append(f'{video_name} --- {video_id}')
                write_in_folder(f'{download_folder}/corrupted_videos.txt', corrupted_videos)
                counter_corrupt_videos += 1
            else:
                stream = yt.streams.filter(only_audio=True).first()
                file_exist = os.path.isfile(f'{download_folder}/{video_name}.{file_format}')

                if not file_exist:
                    # download the file
                    # out_file = stream.download(output_path='downloads/' + folder_name)
                    out_file = stream.download(output_path=download_folder)

                    if out_file:
                        # save the file
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.' + file_format
                        os.rename(out_file, new_file)
                        print(colorama_plus + f' File : {video_name}.{file_format} {colorama.Fore.GREEN} saved !'
                                              f'{colorama_end}')
                else:
                    print(colorama_less + f' File {video_name}.{file_format} {colorama.Fore.YELLOW} already exist '
                                          f'{colorama_end}')

        print(f'{counter_corrupt_videos} videos corrupted')
        print('Corrupted videos => ', corrupted_videos)


# Search if playlist is already registered in uploads folder
def search_existing_registered_playlist(playlist_name):
    return os.path.isfile('uploads/' + playlist_name + '.txt')


# Exclude hidden files for search in folders
def exclude_hidden_files():
    print('hidden files')


def compare_nbr_items_playlists():
    print('compare')


# Main function
def main():
    nbr_pages = 0
    song_list = []
    title.start_program()

    # Display playlists from youtube account
    if args.list:

        # get credentials from youtube
        build = authenticate_youtube()
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

            print('List of playlists found from your account :\n')

            for key, value in playlist_dictionary.items():
                registered = colorama.Fore.RED + ' (Playlist no registered localy) ' + colorama.Style.RESET_ALL
                if value['registered']:
                    registered = colorama.Fore.GREEN + ' (Playlist allready registered localy) ' + colorama.Style.RESET_ALL

                print(colorama_plus, key, '-', value['title'] + registered)

            print(colorama_yellow)
            consent = input('Do you want download a playlist locally ? (Y/N) ')

            if consent == 'Y' or consent == 'y':

                playlist_id = input('Choose playlist by ID : ')
                print(playlist_id)
                print(colorama.Style.RESET_ALL)

                # @todo : add verification for string input
                if 1 <= int(playlist_id) <= len(playlist_dictionary):

                    print(colorama_plus, 'Playlist choose : ', playlist_dictionary[int(playlist_id)]['title'])
                    playlist_items = get_playlists_items(build, playlist_dictionary[int(playlist_id)]['id'])
                    try:
                        next_page_token = playlist_items['nextPageToken']
                    except:
                        next_page_token = ''

                    for item in playlist_items['items']:
                        video_id = item['snippet']['resourceId']['videoId']
                        song = item['snippet']['title'] + " --- " + video_id
                        song_list.append(song)

                    # If there is more than 50 videos in playlist
                    while next_page_token != '':

                        playlist_items_next = get_playlist_items_next(build, playlist_dictionary[int(playlist_id)][
                            'id'], next_page_token)

                        try:
                            next_page_token = playlist_items_next['nextPageToken']
                        except:
                            next_page_token = ''

                        # print('next page token => ', next_page_token)
                        for item in tqdm(playlist_items_next['items']):
                            video_id = item['snippet']['resourceId']['videoId']
                            song = item['snippet']['title'] + " --- " + video_id
                            song_list.append(song)

                    write_in_folder(f"uploads/{playlist_dictionary[int(playlist_id)]['title']}.txt", song_list)

                    # CLear and MAJ datas for while loop after registered a playlist
                    song_list.clear()
                    if search_existing_registered_playlist(playlist_dictionary[int(playlist_id)]['title']):
                        playlist_dictionary[int(playlist_id)]['registered'] = True

                else:
                    print(colorama_less + colorama.Fore.RED + ' Error : Value ' + playlist_id + ' is not valid' +
                          colorama_end + '\n')

            else:
                print('End of program ...')
                break

    # Verify if a playlist is already registered locally (/uploads)
    elif args.registered:

        print(os.listdir("uploads"))

    # Download directly from an ID or url
    elif args.download:

        if args.download != 'download_playlist':
            print('URL is required here')
            # r = requests.get(args.download)
            # print(r)
        else:

            files = os.listdir("uploads")
            files_new = {}
            i = 0
            j = 1
            while i < len(files):
                if files[i][0] != '.':
                    files_new[j] = {'title': files[i]}
                    j = j + 1
                i = i + 1

            print('List of playlists registered locally :' + '\n')
            for key, file in files_new.items():
                print(colorama_plus, key, '-', file['title'])

            # @todo : add verification for string input
            playlist_id = input('\nChoose a file to download by ID (Q to quit) : ')

            if playlist_id == 'q' or playlist_id == 'Q':
                print('End of program ...')
                exit()

            selected_file = files_new[int(playlist_id)]
            print('File selected : ', selected_file['title'])

            while True:
                print('Format available : ')

                for f in settings.DOWNLOAD_VALID_FORMAT:
                    print(colorama_plus + ' - ' + f)
                file_format = input('Please enter the format (leave blank for mp3) : ')

                if file_format == '':
                    file_format = 'mp3'

                if file_format in settings.DOWNLOAD_VALID_FORMAT:
                    download_playlist(selected_file['title'], file_format)
                    break





    # Cut long videos
    elif args.cut:
        print(args.cut)

    elif args.test2:
        url = 'https://www.youtube.com/watch?v=uFnlCzgThS8&ab_channel=ValdSullyvan'
        url2 = 'https://www.youtube.com/watch?v=bxWaWiaQz6w&ab_channel=Yotozz'
        print('je suis args test 2')
        try:

            yt = YouTube(url2)
            # Get video by mime_type
            available = yt.check_availability()
            print(available)
            stream = yt.streams.filter(only_audio=True).first()

            # print(available_video)
        except:
            print('je suis except')
        else:
            print('ici')

        # print(f'Bypasse age {yt.bypass_age_gate()}')
        # yt.check_availability()  # test availability on url
        #
        # print(json.dumps(yt.streams))
        # stream = yt.streams.filter(only_audio=True).first()
        # # download the file
        # try:
        #     print('je suis try')
        #     # out_file = stream.download(output_path='downloads/' + folder_name)
        # except:
        #     print('probleme')



    # Traduce a song
    elif args.test:
        print(args.test)
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

        with ydl:
            result = ydl.extract_info(
                'https://www.youtube.com/watch?v=RLJnsU5VlAY&ab_channel=2nOfficiel',
                download=True  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

        print(video)
        video_url = video['url']
        print(video_url)

    else:
        print('No argument')


if __name__ == "__main__":
    main()
