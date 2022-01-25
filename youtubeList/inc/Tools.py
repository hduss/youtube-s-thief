import os
import youtubeList.colors as colors
from tqdm import tqdm


class Tools:

    def __init__(self):
        print('__init__ Tools\n')


    #Search if the playlist already exist in uploads folder
    @staticmethod
    def search_existing_registered_playlist(playlist_name):
        return os.path.isfile('uploads/' + playlist_name + '.txt')


    # Count total lines in txt files if exist
    # file_path
    def count_registered_song(self, file_path):
        counter = 0
        if self.search_existing_registered_playlist(file_path):
            with open(f'uploads/{file_path}.txt', 'r', encoding="utf8") as lines:
                for line in lines:
                    counter += 1
            # print(f"This is the number of lines in the file : {counter}")
            return counter

        return False


    # registered song name and her youtube id in a txt file
    @staticmethod
    def write_in_folder(file, song_list):
        txt_file = file.split('/')[-1]
        with open(file, 'w', encoding='utf-8') as f:
            for song in tqdm(song_list, desc=f'Writing song in {txt_file}'):
                f.write(song + "\n")

    @staticmethod
    def display_output_playlist(key, value):

        output_string = f'{colors.colorama_less} ' \
                        f'{key} - {value["title"]} ' \
                        f': {colors.colorama_red}Playlist not registered locally ({value["count_registered_file"]}' \
                        f'/{value["count_playlist"]})' \
                        f' {colors.colorama_end}'

        if value['registered']:
            if value['count_playlist'] == value['count_registered_file']:

                output_string = f'{colors.colorama_plus} ' \
                                f'{key} - {value["title"]} ' \
                                f': {colors.colorama_green}Playlist registered locally ' \
                                f'({value["count_registered_file"]}' \
                                f'/{value["count_playlist"]})' \
                                f' {colors.colorama_end}'
            elif value['count_playlist'] != value['count_registered_file']:

                output_string = f'{colors.colorama_warning} ' \
                                f'{key} - {value["title"]} ' \
                                f': {colors.colorama_yellow}Playlist registered locall' \
                                f'y ({value["count_registered_file"]}' \
                                f'/{value["count_playlist"]})' \
                                f' {colors.colorama_end}'

        return output_string

    # Counts the number of lines of the recorded file compared to the number of songs in the Youtube playlist
    # Set complet path
    def count_registered_song(self, file_path):
        counter = 0
        if self.search_existing_registered_playlist(file_path):
            with open(f'uploads/{file_path}.txt', 'r', encoding="utf8") as lines:
                for line in lines:
                    counter += 1
            # print(f"This is the number of lines in the file : {counter}")
            return counter

        return False




