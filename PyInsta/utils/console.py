from getpass import getuser
from time import sleep, strftime
import os
import sys

class Console:
    PURPLE    = '\033[95m'
    CYAN      = '\033[96m'
    DARKCYAN  = '\033[36m'
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    ORANGE    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    ITALIC    = '\x1B[3m'
    DEFAULT   = '\033[0m'
    LINE      = '\033[F'

    COMMAND_LINE = f"{DEFAULT}{ITALIC}{GREEN}pyinsta@{getuser()}:{BLUE}~{os.getcwd().split(getuser())[1]}{DEFAULT}{BOLD}$ "
    BANNER_BRUTE = f"""{BOLD}{RED}
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
                              
                              [{PURPLE}R E A D Y{RED}]"""
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

def runnerBruteBanner(passw,ip,words,prxies,target):
  BANNER_RUNNING_BRUTE = f"""
target>{target}                           {Console.PURPLE}╰─({Console.RED}{strftime("%H:%M:%S")}{Console.PURPLE})─╯
[ {Console.RED}!{Console.PURPLE} ] Wordlist         : {Console.CYAN}{words}{Console.PURPLE} word
[ {Console.RED}!{Console.PURPLE} ] All Worker Proxy : {Console.CYAN}{prxies}{Console.PURPLE} proxy
[ {Console.RED}!{Console.PURPLE} ] Trying Password  : {Console.CYAN}{passw}{Console.PURPLE}
[ {Console.RED}!{Console.PURPLE} ] This Proxy       : {Console.CYAN}{ip}{Console.PURPLE}"""
  return BANNER_RUNNING_BRUTE