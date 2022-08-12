import json
import os
from requests import Session
from time import sleep
from .proxychecker import ProxyChecker
from random import (choice,randint)

class TempMail:
    def __init__(self) -> None:
        super().__init__()
        self.__cookies = {}
        self.__header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Host": "www.fakemail.net",
                "Referer": "https://www.fakemail.net/"
            }
        self.getPHPSESSID()
        self.createAccount()
        # self.inboxRefresh()
    
    def getPHPSESSID(self):
        with Session() as session:
            self.__cookies.update(session.get("https://www.fakemail.net/",verify=False).cookies.get_dict())
    
    def createAccount(self):
        with Session() as session:
            self.__header.update({"Cookie":f"PHPSESSID={self.__cookies['PHPSESSID']}"})
            self.__cookies.update(session.get("https://www.fakemail.net/index/index",verify=False,headers=self.__header).cookies.get_dict())
    
    def inboxRefresh(self):
        with Session() as session:
            self.__header.update({"Cookie":f"PHPSESSID={self.__cookies['PHPSESSID']}; TMA={self.__cookies['TMA']}; wpcc=dismiss"})
            while True:
                os.system("cls")
                print("E-mail: %s" % self.__cookies['TMA'].replace('%40','@'))
                print(json.loads(session.get("https://www.fakemail.net/index/refresh",verify=False,headers=self.__header).text.replace(u'\ufeff',''))[0]['predmet'])
                sleep(2)

class InstagramCreateAccount(TempMail):
    def __init__(self) -> None:
        self.__mail = super().__cookies['TMA'].replace('%40','@')
        self.__redirectcookies = {}

    def redirectEmailSignUp(self):
        with Session() as session:
            header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
            proxy = {"http":f"http://proxy","https":f"http://proxy"}
            self.__redirectcookies.update(session.get("https://www.instagram.com/accounts/emailsignup/",headers=header).cookies.get_dict())
    
    @property
    def __useragents(self):
        dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
        model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
        pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
        i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
        user_agent = f'Instagram {choice(i_version)} Android (30/3.0; {choice(dpi_phone)}dpi; {choice(pxl_phone)}; huawei/google; {choice(model_phone)}; angler; angler; en_US)'
        return user_agent

    def attempt(self):
        with Session() as session:
            session.post("https://www.instagram.com/accounts/web_create_ajax/attempt/")
# to be continued....
