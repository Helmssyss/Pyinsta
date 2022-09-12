from getpass import getuser
from time import strftime
from colorama import (init,Fore,Style)
import os
import sys

init(autoreset=True)
class Console:
    BOLD      = '\033[1m'
    ITALIC    = '\x1B[3m'
    COMMAND_LINE = f"{Fore.RESET}{Style.BRIGHT}{Fore.GREEN}pyinsta@{getuser()}:{Fore.BLUE}~{os.getcwd().split(getuser())[1]}{Fore.RESET}{BOLD}$ "
    BANNER_BRUTE = f"""{BOLD}{Fore.CYAN}
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
                              
                              [{Fore.MAGENTA}R E A D Y{Fore.CYAN}]"""
    BANNER = f"""{Fore.CYAN}
        _____   ________________   __________  ___    __  ___
       /  _/ | / / ___/_  __/   | / ____/ __ \/   |  /  |/  /
       / //  |/ /\__ \ / / / /| |/ / __/ /_/ / /| | / /|_/ / 
     _/ // /|  /___/ // / / ___ / /_/ / _, _/ ___ |/ /  / /  
    /___/_/ |_//____//_/ /_/  |_\____/_/ |_/_/  |_/_/  /_/
                        {Style.BRIGHT}{Fore.GREEN}Helmsys{Fore.RESET}
            {Fore.MAGENTA}https://github.com/Arif-Helmsys{Fore.CYAN}

    [ {Fore.MAGENTA}0{Fore.CYAN} ] Account Info{'':<5} [ {Fore.MAGENTA}e{Fore.CYAN} ] Exit
    [ {Fore.MAGENTA}1{Fore.CYAN} ] Read Message{Fore.CYAN:<10} [ {Fore.MAGENTA}x{Fore.CYAN} ] Logout of account
    """

    MULTI_ACCOUNT_BANNER = f"""{Fore.CYAN}    ____           __
   /  _/___  _____/ /_____ _ 
   / // __ \/ ___/ __/ __ `/
 _/ // / / (__  ) /_/ /_/ /
/___/_/ /_/____/\__/\__,_/
             __  ___      ____  _
            /  |/  /_  __/ / /_(_)
           / /|_/ / / / / / __/ / 
          / /  / / /_/ / / /_/ /  
         /_/  /_/\__,_/_/\__/_/
    ___                               __ 
   /   | ______________  __  ______  / /_
  / /| |/ ___/ ___/ __ \/ / / / __ \/ __/
 / ___ / /__/ /__/ /_/ / /_/ / / / / /_  
/_/  |_\___/\___/\____/\__,_/_/ /_/\__/\n"""

def runnerBruteBanner(passw,ip,words,prxies,target):
  BANNER_RUNNING_BRUTE = f"""
{Fore.MAGENTA}target>{target}                           {Fore.MAGENTA}╰─({Fore.CYAN}{strftime("%H:%M:%S")}{Fore.MAGENTA})─╯
[ {Fore.CYAN}!{Fore.MAGENTA} ] Wordlist         : {Fore.CYAN}{words}{Fore.MAGENTA} word
[ {Fore.CYAN}!{Fore.MAGENTA} ] All Worker Proxy : {Fore.CYAN}{prxies}{Fore.MAGENTA} proxy
[ {Fore.CYAN}!{Fore.MAGENTA} ] Trying Password  : {Fore.CYAN}{passw}{Fore.MAGENTA}
[ {Fore.CYAN}!{Fore.MAGENTA} ] This Proxy       : {Fore.CYAN}{ip}{Fore.MAGENTA}"""
  return BANNER_RUNNING_BRUTE
