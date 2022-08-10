import os
import sys
import shutil
from time import sleep
from PyInsta import (Instagram,Console,Bruter) # Instagram ve Console Sınıfları
from argparse import ArgumentParser
from getpass import getuser
from configparser import ConfigParser

# ?\n╰──────≻

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
                print(f"{Console.ITALIC:<5}Profile Picture:{'':<9} {_['profile_picture']}")
                print(f"{Console.ITALIC:<5}Biography:{'':<16}{_['bio']}")
                print(f"{Console.ITALIC:<5}Follow:{'':<19}{_['follow']}")
                print(f"{Console.ITALIC:<5}Followeed:{'':<16}{_['followeed']}")
                print(f"{Console.ITALIC:<5}This User Following me:{'':<3}{_['is_follow_me']}")
                print(f"{Console.ITALIC:<5}Post Thumbnail:{'':<10} {_['thumbnail']}\n")

            elif _input_ == "1":
                _ = self.readNewDMessages()["info"] # İlk Sıradaki DM mesajını görüldü atmadan okur
                print(f"{Console.ITALIC:<5}Sender:{'':<11} {_['sender']}") # Mesajı Atan
                print(f"{Console.ITALIC:<5}Senders Message:{'':<2}'{_['msg']}'") # Mesajın kendisi
                print(f"{Console.ITALIC:<5}Time:{'':<12} {_['time']}\n")

            elif _input_ == "x":
                shutil.rmtree(f"C:\\Users\\{getuser()}\\Documents\\PyInsta") # Yoldaki klasörü ve içerisindekileri ile siler
                print(f"{Console.RED}Checked out{Console.DEFAULT}")
                sleep(1)
                os.system("cls")
                sys.exit(0)
            elif _input_ == "e":
                print(f"Bye{Console.DEFAULT}")
                sleep(1)
                os.system("cls")
                break

def arguments():
    arg = ArgumentParser(description='How to Using',
                        epilog=f"{Console.RED}First time to login to Instagram >{Console.GREEN}python app.py -u my_user_name -p my_password{Console.DEFAULT}")
    arg.add_argument('-u','--username',help="Instagram Username",type=str)
    arg.add_argument('-p',"--password",help="Instagram Password",type=str)
    arg.add_argument('-px','--proxy',help="Proxy tipini belirtin [socks4, socks5, http] "\
                                          "Ya da elinizde olan proxy dosyasını yazın",type=str)
    arg.add_argument('-v','--victim',help="Kurbanın kullanıcı adı",type=str)
    arg.add_argument('-w','--wordlist',help="Wordlist yolu belirtin",type=str)
    arg.add_argument('-t','--thread',help="Thread Sayısını belirtin [4, 5, 6, ..., 40, ...]",type=int,default=40)
    arg.add_argument('-b',"--brute-force",action='store_const',const="help")
    parse = arg.parse_args()
    return parse

if __name__ == "__main__":
    arguments = arguments()
    if arguments.brute_force == "help":
        print("-t/--thread   : THREAD Number")
        print("-w/--wordlist : WORDLIST")
        print("-v/--victim   : VICTIM")
        print("-px/--proxy   : PROXY TYPE ['http','socks4','socks5'] or PROXY FILE\n")
        print(f"{Console.GREEN}python app.py -v user_name -w wordlist.txt -px proxy_file.txt -t 40{Console.DEFAULT}")

    elif arguments.proxy and arguments.wordlist and arguments.victim:
            Bruter(wordlist=arguments.wordlist,proxy_type=arguments.proxy.lower(),victim=arguments.victim,max_thread=arguments.thread)
    else:
        if not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\.env") and not os.path.exists(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini"):
        # ".env" dosyası ve "account.ini" dosyası yok ise
            try:
                if sys.argv[2] and sys.argv[4]: # kullanıcı adı ve parola girildiyse
                    App(arguments.username,arguments.password)
            except IndexError: # kullanıcı adı ve parola girilmedi ise
                print(f"{Console.RED}Please Login First{Console.DEFAULT}")
        else: # ".env" dosyası ve "account.ini" dosyası var ise
            cfg = ConfigParser() # ConfigParser sınıfından nesne oluşturulur
            cfg.read(f"C:\\Users\\{getuser()}\\Documents\\PyInsta\\account.ini","utf-8") # nesneden okuma methodu çağırılıp içerisine ".ini" dosyasının yolu verilir
            App(cfg["ACCOUNT"]["username"],cfg["ACCOUNT"]["password"])
                        # Kullanıcı Adı  ,    # Parola 