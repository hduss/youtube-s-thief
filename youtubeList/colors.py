import colorama

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