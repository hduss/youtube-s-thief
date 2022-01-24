import youtubeList.title as title
import youtubeList.settings as settings
import os
import colorama
import argparse
import youtube_dl
import pytube.exceptions
from pytube import Playlist, YouTube
from youtubeList.inc.YoutubeApi import YoutubeApi
from youtubeList.inc.Tools import Tools
from youtubeList.inc.Downloader import Downloader

# Colorama init and variables
colorama.init()
colorama_green = colorama.Fore.GREEN
colorama_red = colorama.Fore.RED
colorama_yellow = colorama.Fore.YELLOW
colorama_end = colorama.Style.RESET_ALL

colorama_plus = f'[{colorama_green}+{colorama_end}]'
colorama_less = f'[{colorama_red}+{colorama_end}]'
colorama_warning = f'[{colorama_yellow}!{colorama_end}]'
colorama_less_yellow = f'[{colorama_yellow}-{colorama_end}]'


# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', help='Show all your youtube playlists to save them',
                    action='store_true')
parser.add_argument('-r', '--registered', help='List your locally saved playlists to then download the videos',
                    action="store_true")
parser.add_argument('-t', '--test', help='Argument available for tests',
                    nargs='?', const="download_playlist")
parser.add_argument('-t2', '--test2', help='Second argument available for tests',
                    action='store_true')
parser.add_argument('-d', '--download', help='Download a playlist/video from his ID or from url',
                    nargs='?', const="download_playlist")
parser.add_argument('-c', '--cut', help='cut a video in several song')
args = parser.parse_args()
print(f'Arguments list : {args}')


# Download a playlist from txt file with youtube-dl
def download_playlist_youtube_dl(filename, file_format):
    print(f'Filename => {filename}')
    print(f'Filename => {file_format}')

    with open('uploads/' + filename, encoding="utf8") as lines:
        for line in lines:
            print(line)
            split_line = line.split('---')
            # Exemple => don't become dont in download pytube
            video_name = split_line[0].strip().replace('\'', '').replace('.', '')
            video_id = split_line[1].strip()
            url = 'https://www.youtube.com/watch?v=' + video_id

            # ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
            class MyLogger(object):
                def debug(self, msg):
                    pass

                def warning(self, msg):
                    pass

                def error(self, msg):
                    print(msg)

            def my_hook(d):
                if d['status'] == 'finished':
                    print('Done downloading, now converting ...')

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],

            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])


# Downloading a playlist from .txt file with pytube
def download_playlist(filename, file_format):
    print(f'Filename => {filename}')
    print(f'Filename => {file_format}')

    with open('uploads/' + filename, encoding="utf8") as lines:

        folder_name = filename.split('.txt')[0]
        counter_corrupt_videos = 0
        corrupted_videos = []
        stream = False
        download_folder = f'downloads/{folder_name}/{file_format}'

        for line in lines:
            print(line)

            split_line = line.split('---')
            # Exemple => don't become dont in download pytube
            video_name = split_line[0].strip().replace('\'', '').replace('.', '')
            video_id = split_line[1].strip()
            url = 'https://www.youtube.com/watch?v=' + video_id
            print(f'URL => {url}')

            try:
                yt = YouTube(url)
                yt.check_availability()  # test availability on url
                stream = yt.streams.filter(only_audio=True).first()  # Test for age restricted
            except:
                corrupted_videos.append(f'{video_name} --- {video_id}')
                Tools.write_in_folder(f'{download_folder}/corrupted_videos.txt', corrupted_videos)
                counter_corrupt_videos += 1

            else:
                yt = YouTube(url)
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
                        print(
                            colorama_plus + f' File : {video_name}.{file_format} {colorama.Fore.GREEN} saved !{colorama_end}')
                else:
                    print(colorama_less_yellow + f' File {video_name}.{file_format} {colorama.Fore.YELLOW} already '
                                                 f'exist {colorama_end}')

        print(f'{counter_corrupt_videos} videos corrupted')
        print('Corrupted videos => ', corrupted_videos)


# Counts the number of lines of the recorded file compared to the number of songs in the Youtube playlist
# Set complet path
def count_registered_song(file_path):
    counter = 0
    if search_existing_registered_playlist(file_path):
        with open(f'uploads/{file_path}.txt', 'r', encoding="utf8") as lines:
            for line in lines:
                counter += 1
        # print(f"This is the number of lines in the file : {counter}")
        return counter

    return False


# Count number of video in a playlist on Youtube account
def count_number_of_videos(playlist):
    print('count_number_of_videos function')


# Search if playlist is already registered in uploads folder
def search_existing_registered_playlist(playlist_name):
    return os.path.isfile('uploads/' + playlist_name + '.txt')


# Exclude hidden files for search in folders
def exclude_hidden_files():
    print('hidden files')


def compare_nbr_items_playlists():
    print('compare')


def display_output_playlist(key, value):

    output_string = f'{colorama_less} ' \
                    f'{key} - {value["title"]} ' \
                    f': {colorama_red}Playlist not registered locally ({value["count_registered_file"]}' \
                    f'/{value["count_playlist"]})' \
                    f' {colorama_end}'

    if value['registered']:
        if value['count_playlist'] == value['count_registered_file']:

            output_string = f'{colorama_plus} ' \
                     f'{key} - {value["title"]} ' \
                     f': {colorama_green}Playlist registered locally ({value["count_registered_file"]}' \
                     f'/{value["count_playlist"]})' \
                     f' {colorama_end}'
        elif value['count_playlist'] != value['count_registered_file']:

            output_string = f'{colorama_warning} ' \
                     f'{key} - {value["title"]} ' \
                     f': {colorama_yellow}Playlist registered locally ({value["count_registered_file"]}' \
                     f'/{value["count_playlist"]})' \
                     f' {colorama_end}'

    return output_string


# Main function
def main():
    title.start_program()

    # Display playlists from youtube account
    if args.list:

        # Auth API and get playlists
        yt_api = YoutubeApi()
        playlists = yt_api.get_playlists()
        playlist_dict = yt_api.create_playlists_dict(playlists)

        while True:

            print('List of playlists found from your account :\n')
            for key, value in playlist_dict.items():
                print(display_output_playlist(key, value))

            consent = input(f'\n{colorama_yellow}Do you want registered a playlist locally ? (Y/N){colorama_end} : ')
            if consent == 'Y' or consent == 'y':

                playlist_id = input(f'{colorama_yellow}Choose playlist by ID : {colorama_end}')

                # @todo : add verification for string input
                if 1 <= int(playlist_id) <= len(playlist_dict):
                    print(colorama_plus, 'Playlist choose : ', playlist_dict[int(playlist_id)]['title'])
                    # Set all song in yt_api._song_list
                    yt_api.get_all_items(int(playlist_id))
                    # Write all song in txt file
                    Tools.write_in_folder(f"uploads/{playlist_dict[int(playlist_id)]['title']}.txt",
                                          yt_api.get_song_list())

                    # MAJ datas for next loop
                    playlist_dict[int(playlist_id)]['count_registered_file'] = count_registered_song(
                        playlist_dict[int(playlist_id)]['title'])
                    if Tools.search_existing_registered_playlist(playlist_dict[int(playlist_id)]['title']):
                        playlist_dict[int(playlist_id)]['registered'] = True

                    yt_api.set_song_list([])
                    yt_api.set_playlist_dictionary(playlist_dict)

                else:
                    print(colorama_less + colorama.Fore.RED + ' Error : Value ' + playlist_id + ' is not valid' +
                          colorama_end + '\n')
            else:
                print('End of program ...')
                break


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

            print(f'List of playlists registered locally : \n')
            for key, file in files_new.items():
                print(colorama_plus, key, '-', file['title'])

            # @todo : add verification for string input
            playlist_id = input(f'\n{colorama_yellow}Choose a file to download by ID (Q to quit) : {colorama_end}')

            if 1 <= int(playlist_id) <= len(files_new):
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
                        # download_playlist_youtube_dl(selected_file['title'], file_format)
                        download_playlist(selected_file['title'], file_format)
                        break

            elif playlist_id == 'q' or playlist_id == 'Q':
                print('End of program quit...')
                exit()

            else:
                print('End of program else ...')
                exit()

    # Cut long videos
    elif args.cut:
        print(args.cut)


    # Verify if a playlist is already registered locally (/uploads)
    elif args.registered:
        print(os.listdir("uploads"))


    # Testing
    elif args.test:
        print(args.test)
        # ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
        #
        # with ydl:
        #     result = ydl.extract_info(
        #         'https://www.youtube.com/watch?v=RLJnsU5VlAY&ab_channel=2nOfficiel',
        #         download=True  # We just want to extract the info
        #     )
        #
        # if 'entries' in result:
        #     # Can be a playlist or a list of videos
        #     video = result['entries'][0]
        # else:
        #     # Just a video
        #     video = result
        #
        # print(video)
        # video_url = video['url']
        # print(video_url)

        # file = 'uploads/Liked videos.txt'
        # print(count_registered_song(file))
        #
        # build = authenticate_youtube()
        # playlists = get_playlists(build)
        # print(json.dumps(playlists, indent=2))
        # count_liked_playlist = get_liked_videos(build)['pageInfo']['totalResults']
        # print(json.dumps(liked_playlist['snippet'], indent=2))

        # print(liked_playlist)


        downloader = Downloader(args.test)
        downloader.download_playlist()
        print(f'Downloader object => {downloader}')







    elif args.test2:
        url = 'https://www.youtube.com/watch?v=uFnlCzgThS8&ab_channel=ValdSullyvan'
        url2 = 'https://www.youtube.com/watch?v=bxWaWiaQz6w&ab_channel=Yotozz'
        url3 = 'https://www.youtube.com/watch?v=tO4dxvguQDk'
        url4 = 'https://www.youtube.com/watch?v=HqJ1qP05Si0&ab_channel=Ninho'
        print('je suis args test 2')

        yt = YouTube(url)
        print(yt.title)
        try:
            streams = yt.streams()
        except pytube.exceptions.AgeRestrictedError as restricted:
            print(f'restricted => {restricted}')
            print('age restricted')
        except pytube.exceptions.VideoUnavailable:
            print('unavailable')
        except pytube.exceptions.RegexMatchError:
            print('regex')


        except pytube.exceptions.VideoPrivate:
            print('private video')
        except pytube.exceptions.VideoUnavailable:
            print('test3333')
        else:
            print('je passe ici')

        # yt = YouTube(url2)
        # print(yt.title)
        # print(yt.streams())


        # try:
        #
        #     yt = YouTube(url1)
        #     # print(yt)
        #     # Get video by mime_type
        #     # available = yt.check_availability()
        #     # print(available)
        #     # stream = yt.streams.filter(only_audio=True).first()
        #
        #     # print(available_video)
        # except:
        #     print('je suis except')
        # else:
        #     print('ici')

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


    else:
        print('No argument given')


if __name__ == "__main__":
    main()
