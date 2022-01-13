# Youtube's thief

 [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Allows you to upload audio from youtube videos and playlists,

> development in progress

## Prerequisites
    1 - Create an api key for youtube-api, follow this tutorial : 
    2 - Add your token in a file client_secrets.json in credentials folder
    3 - Launch "python main.py"
    4 - Select your profile from youtube to authenticate 
    5 - A file named token.pickle will be created in the credentials folder for future use

## Environment
    Pyhton3

## How it works
    python main.py --help to have all commands
    python main.py -l to list all your playlist from your account

    The first step is to save the playlists locally :

    
![list of youtube account playlists](public/img/playlists_list.png?raw=true)
    
    (IN PROGRESS)
    Once the playlist is saved, you can download it from the command: 
    => python main.py --download to download playlistys registred locally
    => python main.py --download https://youtube.com?list=zergvrezgreh to download plyalist
    OR unique video


