# Author: Arif "Helmsys"

from threading import Thread
from urllib3 import disable_warnings
from requests import Session
from bs4 import BeautifulSoup
from time import sleep
from .console import Console
from .proxychecker import ProxyChecker
from colorama import (init, Fore)
from datetime import datetime
from random import (choice,randint)
from string import ascii_uppercase
import sys
import uuid
import json
import os

init(autoreset=True)
disable_warnings()
accounts = {}
errcount = 0
usingProxy = False
proxyList = []
class __TempMail(ProxyChecker):
    def __init__(self,prxtype,first:int) -> None:
        global usingProxy
        if first == 1:
            usingProxy = True
            super().__init__(prxtype=prxtype,isProxyPath=True if prxtype not in ['http','socks4','socks5'] else False, filePath=prxtype)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Console.MULTI_ACCOUNT_BANNER)
            for i in self.getWorkerProxy:
                proxyList.append(i)
        
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
        self.getPHPSESSID()
        self.createAccount()
        print(f"\t🟡 {Fore.YELLOW}E-mail: {self.cookies['TMA'].replace('%40','@')}")
        t = Thread(target=self.inboxRefresh,daemon=True)
        t.start()

    def getPHPSESSID(self):
        with Session() as session:
            self.cookies.update(session.get("https://www.fakemail.net/",verify=False).cookies.get_dict())

    def createAccount(self):
        with Session() as session:
            self.__header.update({"Cookie":f"PHPSESSID={self.cookies['PHPSESSID']}"})
            self.cookies.update(session.get("https://www.fakemail.net/index/index",verify=False,headers=self.__header).cookies.get_dict())
            return

    def inboxRefresh(self):
        with Session() as session:
            self.__header.update({"Cookie":f"PHPSESSID={self.cookies['PHPSESSID']}; TMA={self.cookies['TMA']}; wpcc=dismiss"})
            while len(self.verify_code) < 1:
                parsemsg = str(json.loads(session.get("https://www.fakemail.net/index/refresh",verify=False,headers=self.__header).text.replace(u'\ufeff',''))[0]['predmet'])
                for i in parsemsg:
                    if i.isdigit():
                        self.verify_code += i
                sleep(1)

class InstagramCreateAccount(__TempMail):
    def __init__(self,prxtype_:str,first:int) -> None:
        super().__init__(prxtype=prxtype_,first=first)
        self.__prxtype=prxtype_
        self.__mail = self.cookies['TMA'].replace('%40','@')
        self.__redirectcookies = {}

    def redirectEmailSignUp(self):
        # print(f"\t🍪 {Fore.YELLOW}Getting Cookies")
        try:
            with Session() as session:
                header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
                self.__redirectcookies.update(session.get("https://www.instagram.com/accounts/emailsignup/",headers=header).cookies.get_dict())
        except:
            pass

    @property
    def __useragents(self):
        dpi_phone = ['133','320','515','160','640','240','120''800','480','225','768','216','1024']
        model_phone = ['Nokia 2.4','HUAWEI','Galaxy','Unlocked Smartphones','Nexus 6P','Mobile Phones','Xiaomi','samsung','OnePlus']
        pxl_phone = ['623x1280','700x1245','800x1280','1080x2340','1320x2400','1242x2688']
        i_version = ['114.0.0.20.2','114.0.0.38.120','114.0.0.20.70','114.0.0.28.120','114.0.0.0.24','114.0.0.0.41']
        user_agent = f'Instagram {choice(i_version)} Android (30/3.0; {choice(dpi_phone)}dpi; {choice(pxl_phone)}; huawei/google; {choice(model_phone)}; angler; angler; en_US)'
        return user_agent

    def randomPassword(self) -> list:
        with Session() as passw:
            __storage = []
            soup = BeautifulSoup(passw.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/months.txt").content,"lxml")
            for i in soup.find_all("p"):
                __storage.append(i.text.replace("\n","|"))

        for j in __storage:
            __storage = j.split("|")

        __storage.remove("0")
        return __storage

    def attempt(self,count:int,password:str):
        global errcount
        print(f"\t🟡 {Fore.YELLOW}Password: {password}")
        with Session() as session:
            try:
                __header = {
                    "User-Agent":self.__useragents,
                    "x-csrftoken" :self.__redirectcookies['csrftoken']
                    }
                __data = {
                    "enc_password"    : f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{password}",
                    "email"           : self.__mail,
                    "username"        : self.__mail.split('@')[0],
                    "first_name"      : self.__mail.split('@')[0]+choice(list(ascii_uppercase)),
                    "opt_into_one_tap": "false"
                }
                proxy = None
                if self.__prxtype != 'false':
                    choice_proxy = choice(proxyList)
                    proxy = {"http":f"{self.__prxtype}://{choice_proxy}","https":f"{self.__prxtype}://{choice_proxy}"}
                    
                    if self.__prxtype not in ['http','socks4','socks5']:
                        proxy = {"http":f"http://{choice_proxy}","https":f"http://{choice_proxy}"}
                    
                    print(f"\t🟡 {Fore.YELLOW}Proxy:  {choice_proxy}")
                print(f"\t🟡 {Fore.YELLOW}Creating account")
                account_create = session.post("https://www.instagram.com/accounts/web_create_ajax/attempt/",headers=__header,data=__data,cookies=self.__redirectcookies,proxies=proxy)
                assert account_create.status_code == 200
                age_data = {
                        "day"  : str(randint(1,31)),
                        "month": str(randint(1,12)),
                        "year" : str(randint(1919,2000))
                }
                check_Age = session.post('https://www.instagram.com/web/consent/check_age_eligibility/',headers=__header,data=age_data,proxies=proxy)
                assert check_Age.status_code == 200
                device = uuid.uuid4().hex
                verify_data = {
                    'device_id':device,
                    'email':self.__mail
                }
                verify_mail = session.post("https://i.instagram.com/api/v1/accounts/send_verify_email/",headers=__header,data=verify_data,proxies=proxy)
                assert verify_mail.status_code == 200
                while len(self.verify_code) < 1:
                    sleep(1)
                    verify_dataV2 = {
                        'code':self.verify_code,
                        'device_id':device,
                        'email':self.__mail
                    }
                    if len(self.verify_code) > 1:
                        check_code = session.post("https://i.instagram.com/api/v1/accounts/check_confirmation_code/",headers=__header,data=verify_dataV2,proxies=proxy)
                        last_data = {
                            "enc_password":__data["enc_password"],
                            "email":__data["email"],
                            "username":__data["username"],
                            "first_name":__data["first_name"],
                            "month":age_data["month"],
                            "day":age_data["day"],
                            "year":age_data["year"],
                            "client_id":device,
                            "seamless_login_enabled":'1',
                            "tos_version":'eu',
                            "force_sign_up_code":check_code.json()['signup_code']
                        }
                        last_verify = session.post("https://www.instagram.com/accounts/web_create_ajax/",headers=__header,data=last_data,proxies=proxy)
                        
                        accounts.update({count: {"mail" : self.__mail,"password":password,"user_name":__data["username"],
                        "account_created" : last_verify.json()['account_created'],"user_id" : last_verify.json()['user_id'],"status" : last_verify.json()['status']}})

                print(f"\t🟢 {Fore.YELLOW}Account Created")
            except:
                print(f"\t🔴 {Fore.YELLOW}ERR")
                errcount += 1
                

    def writeJsonFile(self):
        with open("users.json","w") as file:
            file.write(json.dumps(accounts))

class MultiAccount:
    def __init__(self) -> None:
        global usingProxy
        # print(f"\t{Fore.CYAN}[ {Fore.MAGENTA}0{Fore.CYAN} ] Follow{'':<8}<{Fore.MAGENTA}Belirtilen Hesap takip edilir{Fore.CYAN}>")
        # print(f"\t{Fore.CYAN}[ {Fore.MAGENTA}1{Fore.CYAN} ] Post Like{'':<5}<{Fore.MAGENTA}Belirtilen hesaptaki postu beğenir{Fore.CYAN}>")
        print(f"\t{Fore.CYAN}[ {Fore.MAGENTA}e{Fore.CYAN} ] Exit\n")

        input_ = input(Console.COMMAND_LINE)
        if input_.lower() == 'e':
                print("Bye")
                sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit(0)

        proxy_input_ = input(Console.PROXY_CMD_LINE)
        if input_.lower() != 'e':
            # try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Console.MULTI_ACCOUNT_BANNER)
                for i in range(1,int(input_)+1):
                    ig = InstagramCreateAccount(prxtype_=proxy_input_,first=i)
                    usingProxy = False
                    ig.redirectEmailSignUp()
                    choice_passw = choice(ig.randomPassword())
                    ig.attempt(count=i,password=choice_passw)

                if accounts != {}:
                    print(f"\n\t🟣 {Fore.YELLOW}Written to users.json")
                    ig.writeJsonFile()

                print(f"\t🟢 {Fore.YELLOW}Finished")
                print(f"\t🟡 {Fore.YELLOW}{errcount} Errors encountered")
                sleep(1)
            # except ValueError:
            #         print(f"\t🔴 {Fore.YELLOW}Undefined")
