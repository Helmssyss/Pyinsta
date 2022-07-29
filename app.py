import os
import sys
import shutil
from time import sleep
from PyInsta import (Instagram,Console) # Instagram ve Console Sınıfları
from argparse import ArgumentParser
from getpass import getuser
from configparser import ConfigParser

class App(Instagram): # Uygulamaya ait Ana Sınıf
    def __init__(self, username: str = ..., password: str = ...) -> None:
        self.__userN = username
        super().__init__(username, password)
        if not self.loginState: # İnstagram hesabına giriş başarılı değil ise
            print(f"{Console.RED}ERROR{Console.DEFAULT}")
        else: # İnstagram hesabına giriş başarılı ise
            os.system("cls")
            print(f"{Console.CYAN}{self.__userN}>{Console.BANNER}")
            self.main()
    
    def main(self): # komutların girildiği ve komutlara göre çıktının üretildiği method
        while True:
            _input_ = input(Console.COMMAND_LINE)
            if _input_ == "0":
                __acc = input(Console.COMMAND_LINE.replace("$","#"))
                self.which_account = __acc
                _ = self.instaAccount()["info"] # belirlenen instagram kullanıcısının bilgileri
                print(f"{Console.ITALIC:<5}Biography:{'':<5} {_['bio']}")
                print(f"{Console.ITALIC:<5}Follow:{'':<7}  {_['follow']}")
                print(f"{Console.ITALIC:<5}Followeed:{'':<5} {_['followeed']}")
                print(f"{Console.ITALIC:<5}Post Thumbnail: {_['thumbnail']}\n")
                if __acc == self.__userN: # belirlenen instagram kullanıcısı eğer sen isen
                    i = input("?\n╰──────≻ Do you want to see your followers: ")
                    if i == "y":
                        self.followees() # Takipçiler
                    elif i == "n":
                        pass

            elif _input_ == "1":
                _ = self.readNewDMessages()["info"] # İlk Sıradaki DM mesajını görüldü atmadan okur
                print(f"{Console.ITALIC:<5}Sender:{'':<11} {_['sender']}") # Mesajı Atan
                print(f"{Console.ITALIC:<5}Senders Message:{'':<2} '{_['msg']}'") # Mesajın kendisi
                print(f"{Console.ITALIC:<5}Time:{'':<12} {_['time']}")

            elif _input_ == "x":
                shutil.rmtree(f"C:\\Users\\{getuser()}\\Documents\\PyInsta") # Yoldaki klasörü ve içerisindekileri ile siler
                print(f"{Console.RED}Checked out{Console.DEFAULT}")
                sleep(1)
                os.system("cls")
                sys.exit(0)

if __name__ == "__main__":
    if not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\.env") and not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini"):
    # ".env" dosyası ve "account.ini" dosyası yok ise
        try:
            arg = ArgumentParser(description='İlk kez Instagrama giriş yapabilmek İçin Argümanları girerek doldurun.',allow_abbrev=False)
            arg.add_argument('-u','--username',required=False,help="Instagram Username",type=str)
            arg.add_argument('-p',"--password",required=False,help="Instagram Password",type=str)
            parse = arg.parse_args()
            if sys.argv[2] and sys.argv[4]: # kullanıcı adı ve parola girildiyse
                App(parse.username,parse.password)
        except IndexError: # kullanıcı adı ve parola girilmedi ise
            print(f"{Console.RED}Please Login First{Console.DEFAULT}")
    else: # ".env" dosyası ve "account.ini" dosyası var ise
        cfg = ConfigParser() # ConfigParser sınıfından nesne oluşturulur
        cfg.read(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini","utf-8") # nesneden okuma methodu çağırılıp içerisine ".ini" dosyasının yolu verilir
        App(cfg["ACCOUNT"]["username"],cfg["ACCOUNT"]["password"])
                     # Kullanıcı Adı  ,    # Parola 