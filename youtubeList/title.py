import colorama

colorama.init()

# def start_download(): nbr_pages = input( colorama.Back.GREEN + "How many pages do you want to download ? (enter
# 'ALL' for entire playlist) " + colorama.Style.RESET_ALL) return int(nbr_pages)


def start_program():
    print_title()
    print(colorama.Fore.MAGENTA + colorama.Style.DIM + 'Version 0.0.1.5\n')
    print('Welcome to youtube\'s thief\n')
    print('Youtube\'s thief allows you to download playlist from your youtube channel\n')
    print('Check python main.py --help OR python main.py -h for informations')
    print(colorama.Style.RESET_ALL)


def print_title():
    LOGO = r'''
                          __        __        _          __  __    _      ____
       __  ______  __  __/ /___  __/ /_  ___ ( )_____   / /_/ /_  (_)__  / __/
      / / / / __ \/ / / / __/ / / / __ \/ _ \|// ___/  / __/ __ \/ / _ \/ /_  
     / /_/ / /_/ / /_/ / /_/ /_/ / /_/ /  __/ (__  )  / /_/ / / / /  __/ __/  
     \__, /\____/\__,_/\__/\__,_/_.___/\___/ /____/   \__/_/ /_/_/\___/_/     
    /____/                                                                    
    
    '''
    print(colorama.Fore.MAGENTA + colorama.Style.NORMAL)
    print(LOGO)
    print(colorama.Style.RESET_ALL)

