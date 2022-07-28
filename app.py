import os
import sys
import shutil
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
                print(f"{'':<5}Biography:{'':<5} {'NaN' if _['bio'] == '' else _['bio']}")
                print(f"{'':<5}Follow:{'':<7}  {_['follow']}")
                print(f"{'':<5}Followeed:{'':<5} {_['followeed']}")
                print(f"{'':<5}Post Thumbnail: https://{LinkParser(URL_Shortened(_['thumbnail'])).parse}\n")

            elif _input_ == "1":
                _ = self.readNewDMessages()["info"]
                print(f"Sender: {_['sender']}\nSenders Message: {_['msg']}")
            
            elif _input_ == "x":
                shutil.rmtree(f"C:\\Users\\{getuser()}\\Documents\\PyInsta")
                print("Checked out")
                break

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
            print("Please Login First")
    else:
        cfg = ConfigParser()
        cfg.read(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini","utf-8")
        App(cfg["ACCOUNT"]["username"],cfg["ACCOUNT"]["password"])
