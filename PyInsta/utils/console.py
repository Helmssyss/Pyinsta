from ast import For
from getpass import getuser
from time import sleep, strftime
from colorama import init,Fore,Style
import os
import sys

init(autoreset=True)
class Console:
    BOLD      = '\033[1m'
    ITALIC    = '\x1B[3m'
    COMMAND_LINE = f"{Fore.RESET}{Style.BRIGHT}{Fore.GREEN}pyinsta@{getuser()}:{Fore.BLUE}~{os.getcwd().split(getuser())[1]}{Fore.RESET}{BOLD}$ "
    BANNER_BRUTE = f"""{BOLD}{Fore.RED}
    ____           __                 
   /  _/___  _____/ /_____ _ 
   / // __ \/ ___/ __/ __ `/
 _/ // / / (__  ) /_/ /_/ /
/___/_/ /_/____/\__/\__,_/
  \t     ____             __       ______                   
  \t    / __ )_______  __/ /____  / ____/___  _____________ 
  \t   / __  / ___/ / / / __/ _ \/ /_  / __ \/ ___/ ___/ _ \\
  \t  / /_/ / /  / /_/ / /_/  __/ __/ / /_/ / /  / /__/  __/
  \t /_____/_/   \__,_/\__/\___/_/    \____/_/   \___/\___/
                              
                              [{Fore.MAGENTA}R E A D Y{Fore.RED}]"""
    BANNER = f"""{Fore.CYAN}
        _____   ________________   __________  ___    __  ___
       /  _/ | / / ___/_  __/   | / ____/ __ \/   |  /  |/  /
       / //  |/ /\__ \ / / / /| |/ / __/ /_/ / /| | / /|_/ / 
     _/ // /|  /___/ // / / ___ / /_/ / _, _/ ___ |/ /  / /  
    /___/_/ |_//____//_/ /_/  |_\____/_/ |_/_/  |_/_/  /_/
                        {Style.BRIGHT}{Fore.GREEN}Helmsys{Fore.RESET}
            {Fore.MAGENTA}https://github.com/Arif-Helmsys{Fore.RED}

    [ {Fore.MAGENTA}0{Fore.RED} ] Account Info{'':<5} [ {Fore.MAGENTA}e{Fore.RED} ] Exit
    [ {Fore.MAGENTA}1{Fore.RED} ] Read Message{Fore.RED:<10} [ {Fore.MAGENTA}x{Fore.RED} ] Logout of account
    """

def runnerBruteBanner(passw,ip,words,prxies,target):
  BANNER_RUNNING_BRUTE = f"""
target>{target}                           {Fore.MAGENTA}╰─({Fore.RED}{strftime("%H:%M:%S")}{Fore.MAGENTA})─╯
[ {Fore.RED}!{Fore.MAGENTA} ] Wordlist         : {Fore.CYAN}{words}{Fore.MAGENTA} word
[ {Fore.RED}!{Fore.MAGENTA} ] All Worker Proxy : {Fore.CYAN}{prxies}{Fore.MAGENTA} proxy
[ {Fore.RED}!{Fore.MAGENTA} ] Trying Password  : {Fore.CYAN}{passw}{Fore.MAGENTA}
[ {Fore.RED}!{Fore.MAGENTA} ] This Proxy       : {Fore.CYAN}{ip}{Fore.MAGENTA}"""
  return BANNER_RUNNING_BRUTE