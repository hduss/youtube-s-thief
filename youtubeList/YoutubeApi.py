class YoutubeApi:

    def __init__(self):
        print('je suis init')
        self.authenticate_youtube()

    @classmethod
    def authenticate_youtube(cls):
        print('je suis auth')

    @classmethod
    def get_playlist(cls):
        print('je suis get playlist')