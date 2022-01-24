import youtubeList.settings as setting

class Downloader:

    def __init__(self, downloader):

        print(f'downloader => {downloader}')
        if downloader in setting.DOWNLOADER:
            print('Valid downloader')
            self._downloader = downloader

        else:
            print('Invalid downloader')



    def download_playlist(self, txt_file):
        print(f'Txt file => {txt_file}')



