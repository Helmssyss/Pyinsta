import os
import sys
import shutil
from time import sleep
from PyInsta import (Instagram,Console)
from argparse import ArgumentParser
from getpass import getuser
from configparser import ConfigParser
from PyInsta.utils import (URL_Shortened,LinkParser)

class App(Instagram):
    def __init__(self, username: str = ..., password: str = ...) -> None:
        self.__userN = username
        super().__init__(username, password)
        if not self.loginState:
            print("ERROR")
        else:
            os.system("cls")
            print(f"{Console.CYAN}{self.__userN}>")
            print(Console.BANNER)
            self.main()
    
    def main(self):
        while True:
            _input_ = input(Console.COMMAND_LINE)
            if _input_ == "0":
                self.which_account = input(Console.COMMAND_LINE.replace("$","#"))
                _ = self.instaAccount()["info"]
                print(f"{Console.ITALIC:<5}Biography:{'':<5} {'NaN' if _['bio'] == '' else _['bio']}")
                print(f"{Console.ITALIC:<5}Follow:{'':<7}  {_['follow']}")
                print(f"{Console.ITALIC:<5}Followeed:{'':<5} {_['followeed']}")
                print(f"{Console.ITALIC:<5}Post Thumbnail: https://{LinkParser(URL_Shortened(_['thumbnail'])).parse}\n")

            elif _input_ == "1":
                _ = self.readNewDMessages()["info"]
                print(f"{Console.ITALIC:<5}Sender: {_['sender']}")
                print(f"{Console.ITALIC:<5}Senders Message: {_['msg']}")
            
            elif _input_ == "x":
                shutil.rmtree(f"C:\\Users\\{getuser()}\\Documents\\PyInsta")
                print(f"{Console.RED}Checked out{Console.DEFAULT}")
                sleep(1)
                sys.exit(0)

if __name__ == "__main__":
    if not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\.env") and not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini"):
        try:
            arg = ArgumentParser()
            arg.add_argument('--username',help="Instagram Username",type=str)
            arg.add_argument("--password",help="Instagram Password",type=str)
            parse = arg.parse_args()
            if sys.argv[2] and sys.argv[4]:
                App(parse.username,parse.password)
        except IndexError:
            print(f"{Console.RED}Please Login First{Console.DEFAULT}")
    else:
        cfg = ConfigParser()
        cfg.read(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini","utf-8")
        App(cfg["ACCOUNT"]["username"],cfg["ACCOUNT"]["password"])
