import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from tqdm import tqdm
from youtubeList.inc.Tools import Tools

class YoutubeApi:

    liked_videos = 'Liked videos'

    # Init call authenticate_youtube to log user directly
    def __init__(self):
        self.build = self.authenticate_youtube()
        self.Tools = Tools()
        self._song_list = []
        self._playlist_dictionary = {}


    # Authentication to API && credentials management
    @staticmethod
    def authenticate_youtube():
        # print('je suis authenticate_youtube')
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


    # Create output of dictionnary of all playlists account
    # Liked videos needs to be add manually
    def create_playlists_dict(self, playlists):

        # Add liked videos in dictionary at 1st key
        self._playlist_dictionary[1] = {
            'title': 'Liked videos',
            'id': 'LL',
            'registered': self.Tools.search_existing_registered_playlist(self.liked_videos),
            'count_playlist': self.get_liked_videos()['pageInfo']['totalResults'],
            'count_registered_file':
                (self.Tools.count_registered_song('Liked videos') if self.Tools.search_existing_registered_playlist(self.liked_videos) else 0)
        }

        for ids, items in enumerate(playlists['items'], start=2):
            playlist_title = items['snippet']['localized']['title']

            self._playlist_dictionary[ids] = {
                'title': playlist_title,
                'id': items['id'],
                'registered': self.Tools.search_existing_registered_playlist(playlist_title),
                'count_playlist': items['contentDetails']['itemCount'],
                'count_registered_file':
                    (self.Tools.count_registered_song(playlist_title) if self.Tools.search_existing_registered_playlist(
                        playlist_title) else 0)
            }

        return self._playlist_dictionary


    # Get first page result of a playlist by his ID
    def get_playlists_items(self, playlist_id):
        request = self.build.playlistItems().list(
            part='contentDetails, snippet',
            playlistId=playlist_id,
            maxResults=50
        )
        resp = request.execute()  # Query execution
        return resp


    # Get next results page of a playlist
    def get_playlist_items_next(self, playlist_id, next_page_token):
        request = self.build.playlistItems().list(
            part='contentDetails, snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        resp = request.execute()  # Query execution
        return resp


    # Get all playlist from youutbe account
    def get_playlists(self):
        request = self.build.playlists().list(
            part="snippet, contentDetails",
            mine="true",
            maxResults=50,
        )
        resp = request.execute()  # Query execution
        return resp


    # Get all items from a playlist from his ID
    def get_all_items(self, playlist_id):

        playlist_yt_id = self._playlist_dictionary[int(playlist_id)]['id']
        playlists_items_first = self.get_playlists_items(playlist_yt_id)

        try:
            next_page_token = playlists_items_first['nextPageToken']
        except:
            next_page_token = ''

        for item in playlists_items_first['items']:
            video_id = item['snippet']['resourceId']['videoId']
            song = item['snippet']['title'] + " --- " + video_id
            self._song_list.append(song)

            # If there is more than 50 videos in the playlist
            while next_page_token != '':
                playlist_items_next = self.get_playlist_items_next(playlist_yt_id, next_page_token)
                try:
                    next_page_token = playlist_items_next['nextPageToken']
                except:
                    next_page_token = ''

                for item in tqdm(playlist_items_next['items']):
                    video_id = item['snippet']['resourceId']['videoId']
                    song = item['snippet']['title'] + " --- " + video_id
                    self._song_list.append(song)

        return self._song_list


    def get_liked_videos(self):
        request = self.build.videos().list(
            part='contentDetails, snippet',
            myRating='like',
            maxResults=50
        )
        resp = request.execute()  # Query execution
        return resp


    ## Getters and Setters

    def get_song_list(self):
        return self._song_list

    def set_song_list(self, song_list):
        self._song_list = song_list

    def get_playlist_dictionary(self):
        return self._playlist_dictionary

    def set_playlist_dictionary(self, playlist_dictionary):
        self._playlist_dictionary = playlist_dictionary