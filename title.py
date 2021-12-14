import colorama

colorama.init()


def start_program():
    print('Une page Contient 50 vidéos')
    nbr_pages = input("Combien de pages souhaitez-vous télécharger ? ")
    return int(nbr_pages)


def print_title():
    print(colorama.Fore.RED + colorama.Style.NORMAL)
    print("                         __          __         _          __   __     _        ____")
    print("   __  __ ____   __  __ / /_ __  __ / /_   ___ ( )_____   / /_ / /_   (_)___   / __/")
    print("  / / / // __ \ / / / // __// / / // __ \ / _ \|// ___/  / __// __ \ / // _ \ / /_  ")
    print(" / /_/ // /_/ // /_/ // /_ / /_/ // /_/ //  __/ (__  )  / /_ / / / // //  __// __/  ")
    print(" \__, / \____/ \__,_/ \__/ \__,_//_.___/ \___/ /____/   \__//_/ /_//_/ \___//_/     ")
    print("/____/ ")

    print(colorama.Style.RESET_ALL)



