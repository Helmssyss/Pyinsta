from getpass import getuser
import os
from time import strftime

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

    COMMAND_LINE = f"{DEFAULT}{ITALIC}{GREEN}pyinsta@{getuser()}:{BLUE}~{os.getcwd().split(getuser())[1]}{DEFAULT}{BOLD}$ "
    BANNER_BRUTE = f"""{RED}
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
                           {ITALIC}{GREEN}Helmsys{DEFAULT}
                 {PURPLE}https://github.com/Arif-Helmsys{RED}

        [ {PURPLE}x{RED} ] Exit
    """
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
def runnerBrute(passw,ip):
  BANNER_RUNNING_BRUTE = f"""
    ____           __                                         {strftime("%H:%M:%S")}
   /  _/___  _____/ /_____ _ 
   / // __ \/ ___/ __/ __ `/
 _/ // / / (__  ) /_/ /_/ /
/___/_/ /_/____/\__/\__,_/
  \t     ____             __       ______                   
  \t    / __ )_______  __/ /____  / ____/___  _____________ 
  \t   / __  / ___/ / / / __/ _ \/ /_  / __ \/ ___/ ___/ _ \\
  \t  / /_/ / /  / /_/ / /_/  __/ __/ / /_/ / /  / /__/  __/
  \t /_____/_/   \__,_/\__/\___/_/    \____/_/   \___/\___/
                                     {Console.ITALIC}{Console.GREEN}Helmsys{Console.DEFAULT}
                       {Console.PURPLE}https://github.com/Arif-Helmsys{Console.RED}
              
    {Console.RED}[ {Console.PURPLE}!{Console.PURPLE} {Console.RED}] Trying Password : {Console.CYAN}{passw}       {Console.RED}[ {Console.PURPLE}!{Console.PURPLE} {Console.RED}] Blocked IP: {Console.CYAN}{ip}

"""
  return BANNER_RUNNING_BRUTE