import os

from tqdm import tqdm

class Tools:

    def __init__(self):
        print('__init__ Tools')


    #Search if the playlist already exist in uploads folder
    def search_existing_registered_playlist(self, playlist_name):
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



