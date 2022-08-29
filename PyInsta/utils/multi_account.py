# to be continued...

import json
import os
from pprint import pprint
from threading import Thread
from urllib3 import disable_warnings
from requests import Session
from time import sleep
from .console import Console
# from .proxychecker import ProxyChecker
from datetime import datetime
from random import (choice,randint)
from string import ascii_uppercase
import uuid

disable_warnings()


class TempMail:
    def __init__(self) -> None:
        print(Console.MULTI_ACCOUNT_BANNER)
        input("Merhaba: ")
        self.verify_code = ""
        self.cookies = {}
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
        Thread(target=self.inboxRefresh).start()

    def getPHPSESSID(self):
        with Session() as session:
            self.cookies.update(session.get("https://www.fakemail.net/",verify=False).cookies.get_dict())
    
    def createAccount(self):
        with Session() as session:
            self.__header.update({"Cookie":f"PHPSESSID={self.cookies['PHPSESSID']}"})
            self.cookies.update(session.get("https://www.fakemail.net/index/index",verify=False,headers=self.__header).cookies.get_dict())

    def inboxRefresh(self):
        with Session() as session:
            self.__header.update({"Cookie":f"PHPSESSID={self.cookies['PHPSESSID']}; TMA={self.cookies['TMA']}; wpcc=dismiss"})
            while True:
                # os.system("cls")
                print("E-mail: %s\n" % self.cookies['TMA'].replace('%40','@'))
                parsemsg = str(json.loads(session.get("https://www.fakemail.net/index/refresh",verify=False,headers=self.__header).text.replace(u'\ufeff',''))[0]['predmet'])
                for i in parsemsg:
                    if i.isdigit():
                        self.verify_code += i
                print(self.verify_code)
                if len(self.verify_code) > 1:
                    break
                sleep(2)

class InstagramCreateAccount(TempMail):
    def __init__(self) -> None:
        super().__init__()
        self.__mail = self.cookies['TMA'].replace('%40','@')
        self.__redirectcookies = {}
        self.redirectEmailSignUp()
        self.attempt()

    def redirectEmailSignUp(self):
        print("sa redirectEmailSignUp")
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
        print("mrb attempt")
        with Session() as session:
            __header = {
                "User-Agent":self.__useragents,
                "x-csrftoken" :self.__redirectcookies['csrftoken']
                }
            __data = {
                "enc_password"    : f"PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:password",
                "email"           : self.__mail,
                "username"        : self.__mail.split('@')[0],
                "first_name"      : self.__mail.split('@')[0]+choice(list(ascii_uppercase)),
                "opt_into_one_tap": "false"
                }
            account_create = session.post("https://www.instagram.com/accounts/web_create_ajax/attempt/",headers=__header,data=__data,cookies=self.__redirectcookies)
            assert account_create.status_code == 200
            age_data = {
                "day"  : str(randint(1,31)),
                "month": str(randint(1,12)),
                "year" : str(randint(1919,2000))
            }
            check_Age = session.post('https://www.instagram.com/web/consent/check_age_eligibility/',headers=__header,data=age_data)
            assert check_Age.status_code == 200
            device = uuid.uuid4()
            verify_data = {
                'device_id':device,
                'email':self.__mail
                }
            verify_mail = session.post("https://i.instagram.com/api/v1/accounts/send_verify_email/",headers=__header,data=verify_data)
            assert verify_mail.status_code == 200
            print("bitti")
            #     verify_dataV2 = {
            #         'code':self.verify_code,
            #         'device_id':device,
            #         'email':self.__mail
            #     }
            #     last_verify = session.post("https://www.instagram.com/accounts/web_create_ajax/",headers=__header,data=verify_dataV2)
            # if last_verify.status_code == 200:
            #     print("bitti")
           
        
# to be continued...
