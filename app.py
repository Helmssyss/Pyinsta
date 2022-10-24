# Author: Arif "Helmsys"
# Python Version : 3.9.x

from platform import python_version
from colorama import init,Fore
from time import sleep
from PyInsta import (Instagram, Console, Bruter, MultiAccount)
from argparse import ArgumentParser
from getpass import getuser
from configparser import ConfigParser
import os
import sys
import shutil

init(autoreset=True) # Colorama
class App(Instagram):
    def __init__(self, username: str = ..., password: str = ...) -> None:
        self.__userN = username
        super().__init__(username, password)
        if(not self.loginState):
            print(f"{Fore.RED}ERROR{Fore.RESET}")

        else:
            os.system("cls")
            print(f"{Fore.CYAN}{self.__userN}>{Console.BANNER}")
            self.main()

    def main(self):
        while(True):
            _input_ = input(Console.COMMAND_LINE)
            if(_input_ == "0"):
                __acc = input(Console.COMMAND_LINE.replace("$","#"))
                self.which_account = __acc
                _ = self.instaAccount()["info"]
                print(f"{Console.ITALIC:<5}Profile Picture:{'':<9} {_['profile_picture']}")
                print(f"{Console.ITALIC:<5}Biography:{'':<16}{_['bio']}")
                print(f"{Console.ITALIC:<5}Follow:{'':<19}{_['follow']}")
                print(f"{Console.ITALIC:<5}Followeed:{'':<16}{_['followeed']}")
                print(f"{Console.ITALIC:<5}This User Following me:{'':<3}{_['is_follow_me']}")
                print(f"{Console.ITALIC:<5}Post Thumbnail:{'':<10} {_['thumbnail']}\n")

            elif (_input_ == "1"):
                _ = self.readNewDMessages()["info"]
                print(f"{Console.ITALIC:<5}Sender:{'':<11} {_['sender']}")
                print(f"{Console.ITALIC:<5}Senders Message:{'':<2}'{_['msg']}'")
                print(f"{Console.ITALIC:<5}Time:{'':<12} {_['time']}\n")

            elif(_input_ == "x"):
                shutil.rmtree(f"C:\\Users\\{getuser()}\\Documents\\PyInsta")
                print(f"{Fore.RED}Checked out{Fore.RESET}")
                sleep(1)
                os.system("cls")
                sys.exit(0)

            elif(_input_ == "e"):
                print(f"Bye{Fore.RESET}")
                sleep(1)
                os.system("cls")
                break

def arguments():
    arg = ArgumentParser(description='How to Using',
                        epilog=f"{Fore.RED}First time to login to Instagram > {Fore.GREEN}python app.py -u my_user_name -p my_password{Fore.RESET}")
    arg.add_argument('-u','--username',help="Instagram Username",type=str)
    arg.add_argument('-p',"--password",help="Instagram Password",type=str)
    arg.add_argument('-px','--proxy',help="Specify proxy type [socks4, socks5, http] "\
                                          "or write the proxy file you have",type=str)
    arg.add_argument('-v','--victim',help="Victim username",type=str)
    arg.add_argument('-w','--wordlist',help="Specify wordlist path",type=str)
    arg.add_argument('-t','--thread',help="Specify Number of Threads [4, 5, 6, ..., 40, ...]",type=int,default=40)
    arg.add_argument('-b',"--brute-force",action='store_const',const="help")
    arg.add_argument("--create-account",help="Create Instagram Multi Account",action='store_const',const="help")
    parse = arg.parse_args()
    return parse

if(__name__ == "__main__"):
    if(float(str(python_version()[:3])) == 3.9):
        arguments = arguments()
        if(arguments.brute_force == "help"):
            print("-t/--thread   : THREAD Number")
            print("-w/--wordlist : WORDLIST")
            print("-v/--victim   : VICTIM")
            print("-px/--proxy   : PROXY TYPE ['http','socks4','socks5'] or PROXY FILE\n")
            print(f"{Fore.GREEN}python app.py -v user_name -w wordlist.txt -px proxy_file.txt -t 40{Fore.RESET}")

        elif(arguments.create_account):
            print(Console.MULTI_ACCOUNT_BANNER)
            MultiAccount()

        elif(arguments.proxy and arguments.wordlist and arguments.victim):
                Bruter(wordlist=arguments.wordlist,proxy_type=arguments.proxy.lower(),victim=arguments.victim,max_thread=arguments.thread)

        else:
            if(not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\.env") and not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini")):
                try:
                    if(sys.argv[2] and sys.argv[4]):
                        App(arguments.username,arguments.password)
                except IndexError:
                    print(f"{Fore.RED}Please Login First{Fore.RESET}")

            else:
                cfg = ConfigParser()
                cfg.read(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini","utf-8")
                App(cfg["ACCOUNT"]["username"],cfg["ACCOUNT"]["password"])

    else:
        print(f"{Fore.RED}Only works in 3.9{Fore.RESET}")