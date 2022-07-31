from getpass import getuser
import os

class Console:
    PURPLE    = '\033[95m'
    CYAN      = '\033[96m'
    DARKCYAN  = '\033[36m'
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    ITALIC    = '\x1B[3m'
    DEFAULT   = '\033[0m'

    COMMAND_LINE = f"{DEFAULT}{ITALIC}{GREEN}pyinsta@{getuser()}:{BLUE}~{os.getcwd().split(getuser())[1]}{DEFAULT}{BOLD}$ "
    BANNER = f"""{CYAN}
    _____   ________________   __________  ___    __  ___
   /  _/ | / / ___/_  __/   | / ____/ __ \/   |  /  |/  /
   / //  |/ /\__ \ / / / /| |/ / __/ /_/ / /| | / /|_/ / 
 _/ // /|  /___/ // / / ___ / /_/ / _, _/ ___ |/ /  / /  
/___/_/ |_//____//_/ /_/  |_\____/_/ |_/_/  |_/_/  /_/
                    {ITALIC}{GREEN}Helmsys{DEFAULT}
        {PURPLE}https://github.com/Arif-Helmsys{RED}

[ {PURPLE}0{RED} ] Account Info{'':<5} [ {PURPLE}e{RED} ] Exit
[ {PURPLE}1{RED} ] Read Message{RED:<10} [ {PURPLE}x{RED} ] Logout of account
"""