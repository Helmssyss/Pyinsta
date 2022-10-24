# Author: Arif "Helmsys"

from time import sleep
from .console import Console
from .constants import *
from colorama import (init, Fore)
from datetime import datetime
from random import (choice,randint)
from string import ascii_uppercase
import asyncio
import aiohttp
import sys
import uuid
import json
import os

init(autoreset=True)
accounts = {}
errcount = 0
usingProxy = False
proxyList = []
class __TempMail:
    def __init__(self) -> None:
        print(f"\t🟡 {Fore.YELLOW}Creating E-Mail")
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

    async def getCookies(self):
        await asyncio.gather(self.__getPHPSESSID(),self.__createAccount())

    async def __getPHPSESSID(self):
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            async with session.get("https://www.fakemail.net/") as response:
                cookies = session.cookie_jar.filter_cookies("https://www.fakemail.net/").items()
                for key, cookie in cookies:
                    self.cookies.update({cookie.key: cookie.value})

    async def __createAccount(self):
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(),headers=self.__header) as session:
            async with session.get("https://www.fakemail.net/index/index") as response:
                self.__header.update({"Cookie":f"PHPSESSID={self.cookies['PHPSESSID']}"})
                cookies = session.cookie_jar.filter_cookies("https://www.fakemail.net/index/index").items()
                for key, cookie in cookies:
                    self.cookies.update({cookie.key: cookie.value})
                self.__header.update({"Cookie":f"PHPSESSID={self.cookies['PHPSESSID']}; TMA={self.cookies['TMA']}; wpcc=dismiss"})

    async def inboxRefresh(self):
        async with aiohttp.ClientSession() as session:
            while len(self.verify_code) < 1:
                response = await session.get("https://www.fakemail.net/index/refresh",headers=self.__header)
                result = await response.text()
                result = result.replace(u'\ufeff','')
                parsemsg = json.loads(result)[0]['predmet']
                print(parsemsg)
                for i in parsemsg:
                    if i.isdigit():
                        self.verify_code += i

class __CreateAccount(__TempMail):
    def __init__(self) -> None:
        super().__init__()
        self.__redirectcookies = {}
    
    async def __redirectEmailSignUp(self) -> None: # CSRFTOKEN alınır
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            __header__ = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
            async with session.get("https://i.instagram.com/api/v1/web/login_page/",headers=__header__) as _:
                __cookies__ = session.cookie_jar.filter_cookies("https://i.instagram.com/api/v1/web/login_page/").items()
                for key, cookie in __cookies__:
                    self.__redirectcookies.update({cookie.key : cookie.value})
    @property
    def __useragents(self) -> str:
        dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
        model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
        pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
        i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
        user_agent = f'Instagram {choice(i_version)} Android (30/3.0; {choice(dpi_phone)}dpi; {choice(pxl_phone)}; huawei/google; {choice(model_phone)}; angler; angler; en_US)'
        return user_agent

    async def getRandomPassword(self) -> str: # Hazırlanan listeden rastgele bir parolayı çeker
        async with aiohttp.ClientSession() as session:
            __response = await session.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/months.txt")
            __result = await __response.text()
        return choice(__result.split('\n'))

    async def instAttempt(self,count:int): # Alınan bilgiler doğrultusunda instagrama kayıt olma ve giriş işlemi yapar
        await self.__redirectEmailSignUp()
        await asyncio.sleep(.30)
        async with aiohttp.ClientSession() as session:
            self.__mail = self.cookies['TMA'].replace('%40','@')
            __password = await self.getRandomPassword()
            __header = {
                "User-Agent":self.__useragents,
                "x-csrftoken" :self.__redirectcookies['csrftoken']
            }
            __data = {
                "enc_password"    : f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{__password}",
                "email"           : self.__mail,
                "username"        : self.__mail.split('@')[0],
                "first_name"      : self.__mail.split('@')[0]+choice(list(ascii_uppercase)),
                "opt_into_one_tap": "false"
            }
            __age_data = {
                "day"  : str(randint(1,31)),
                "month": str(randint(1,12)),
                "year" : str(randint(1919,2000))
            }
            device = uuid.uuid4().hex
            __verify_data = {
                'device_id':device,
                'email':self.__mail
            }
            __account_create__ = await session.post(ATTEMPT,headers=__header,data=__data,cookies=self.__redirectcookies)
            await session.post(CHECKAGELIGIBILITY,headers=__header,data=__age_data)
            await asyncio.sleep(.30)
            await session.post(VERIFYMAIL,headers=__header,data=__verify_data)
            while len(self.verify_code) < 1:
                print("while döngüsünde")
                await asyncio.sleep(.30)
                __verifydataV2 = {
                    'code':self.verify_code,
                    'device_id':device,
                    'email':self.__mail
                }
                if len(self.verify_code) > 1:
                    __check_code = await session.post(CHECKCODE,headers=__header,data=__verifydataV2)
                    __check_code = await __check_code.json()
                    last_data = {
                        "enc_password":__data["enc_password"],
                        "email":__data["email"],
                        "username":__data["username"],
                        "first_name":__data["first_name"],
                        "month":__age_data["month"],
                        "day":__age_data["day"],
                        "year":__age_data["year"],
                        "client_id":device,
                        "seamless_login_enabled":'1',
                        "tos_version":'eu',
                        "force_sign_up_code":__check_code['signup_code']
                        }
                    last_verify = await session.post(LASTVERIFY,headers=__header,data=last_data)
                    if last_verify.status == 200:
                        last_verify = await last_verify.json()
                        await asyncio.sleep(.30)
                        print("Hesap oluşturuldu")
                        accounts.update(
                            {
                                count: {
                                    "mail" : self.__mail,
                                    "password":__password,
                                    "user_name":__data["username"],
                                    "account_created" : last_verify['account_created'],
                                    "user_id" : last_verify['user_id'],
                                    "status" : last_verify['status']}})
            print("while döngüsünden çıkıldı")
            self.verify_code = ''
            
    def writeJsonFile(self):
        with open("users.json","w") as file:
            file.write(json.dumps(accounts,indent=4))

class MultiAccount(__CreateAccount):
    def __init__(self) -> None:
        print(f"\t{Fore.CYAN}[ {Fore.MAGENTA}e{Fore.CYAN} ] Exit\n")
        input_ = input(Console.COMMAND_LINE)
        if input_.lower() == 'e':
                print("Bye")
                sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit(0)

        if input_.lower() != 'e':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Console.MULTI_ACCOUNT_BANNER)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__subinit__(input_))
    
    async def __subinit__(self,input_:int):
        try:
            super().__init__()
            for _ in range(int(input_)):
                print("Ana döngü",_)
                await self.getCookies()
                await asyncio.sleep(.30)
                await asyncio.gather(asyncio.create_task(self.instAttempt(_)),asyncio.create_task(self.inboxRefresh()))

            if accounts != {}:
                self.writeJsonFile()

        except ValueError:
            print("Adet Girin!")