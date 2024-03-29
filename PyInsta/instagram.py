import os
import requests
import json
import re

from datetime import datetime
from fake_useragent import UserAgent # user-agent sınıfı
from configparser import ConfigParser
from .libs import(URL_Shortened,LinkParser)
from getpass import getuser
from dotenv import dotenv_values
from bs4 import BeautifulSoup

class Instagram:
    def __init__(self,username:str=...,password:str=...) -> None:
        self.__username = username
        self.__password = password
        self.__cookies = None # her methoddan erişebilmek adına başlangıç değerini "None" olarak atıyorum
        self.loginState = True # Instagram hesabı ile başarılı bir şekilde giriş yapılıp yapılmadığını kontrol ettiğim değişken
        self.__followeed = 0 # Takipçi sayısını saklayabileceğim değişken
        self.__follow = 0 # Takip ettiği kişi sayısını saklayabileceğim değişken
        self.__userID = 0 # Kullanıcının user ID sine ulaşabilmek için kullandığım değişken
        self.__cfg = ConfigParser() # ".ini" dosyasının içeriğine değer yazabilmek için bu sınıfı dahil edip bundan bir obje oluşturuyorum
        if not os.path.exists(r".\account.ini") and not os.path.exists(r".\.env"):
            # "account.ini" ve ".env" yok ise
            __response = requests.get("https://www.instagram.com/accounts/login/") # login sayfasına gidilir
            self.__cookies = __response.cookies.get_dict() # gidilen sayfadan cookieler çekilir
            __loginR = self.__login # cookieler çekildikten sonra instagram kullanıcı adı ve parola ile giriş işlemi gerçekleştirilir
            if self.loginState: # giriş işlemi başarılı ise
                os.system("cls") # Terminal ekranını temizler
                with open(r".\.env","w",encoding="utf-8") as env:
                    with open(r".\account.ini","w",encoding="utf-8") as ini_file:
                        self.__cfg["ACCOUNT"] = __loginR[0] # döndürülen listedeki ilk sözlük verisini yazdırıyorum
                        self.__cfg.write(ini_file) # klasör içerisine ".ini" dosyası yazılır
                        env.write(f"SESSION_ID={__loginR[1]['sessionid']}") # klasör içerisine ".env" dosyası yazılır
                                                                            # klasör içerisine döndürülen listedeki ikinci sözlük verisini yazdırıyorum
    
    def getCSRFtoken(self):
        with requests.Session() as session:
            header = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"
            }
            URL = "https://www.instagram.com/accounts/login/"
            response = session.get(URL,headers=header)
            soup = BeautifulSoup(response.content,"lxml")
            regex = r".*csrf_token\":\"([^\"]+)\".*"
            scraping_script_tags = soup.find_all("script")
            for i in range(len(scraping_script_tags)):
                for j in scraping_script_tags[i]:
                    try:
                        token = j.split("XIGSharedData")[1][5:].replace('\\','')
                        match = re.match(regex, token)
                        if match:
                            return match.group(1)
                    except IndexError:
                        continue

    @property
    def __login(self) -> dict: # giriş işlemi
        csrfToken = self.getCSRFtoken()
        print("CSRF TOKEN ",csrfToken)
        __data = {
            'username' : self.__username,
            'enc_password' : f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{self.__password}',
            'queryParams' : {},
            'optIntoOneTap' : 'false'
        }
        __header = {
            "User-Agent" : UserAgent().random, # rastgele bir user-agent tanımlıyorum
            "X-Requested-With" : "XMLHttpRequest",
            "Referer" : "https://www.instagram.com/accounts/login/",
            "x-csrftoken" : csrfToken
        }
        __response = requests.post("https://www.instagram.com/accounts/login/ajax/",data=__data,headers=__header) # ilgili linke post işlemi yapıyorum
        __json_data = json.loads(__response.text)
        if __json_data["authenticated"]:
            json_resp = __response.cookies.get_dict()
            return [
                {
                    "username":self.__username, # kullanıcı adı
                    "password":str(self.__password), # parola
                    "csrftoken":json_resp["csrftoken"], # cookie
                    "ds_user_id":json_resp["ds_user_id"], # cookie
                    "ig_did":json_resp["ig_did"], # cookie
                    "mid":json_resp["mid"], # cookie
                    "rur":json_resp["rur"] # cookie
                },
                {
                    "sessionid":json_resp["sessionid"] # cookie
                }
                   ]
        else: 
            self.loginState = False

    @property
    def __readConfig(self) -> dict:
        self.__cfg.read(r".\account.ini",'utf-8')
        return {
                    "csrftoken" : self.__cfg["ACCOUNT"]["csrftoken"],
                    "ds_user_id" : self.__cfg["ACCOUNT"]["ds_user_id"],
                    "ig_did" : self.__cfg["ACCOUNT"]["ig_did"],
                    "mid" : self.__cfg["ACCOUNT"]["mid"],
                    "rur" : self.__cfg["ACCOUNT"]["rur"],
                    "sessionid" : dotenv_values(r".\.env")["SESSION_ID"]
               }
    @property
    def which_account(self):
        return self.__username
    
    @which_account.setter
    def which_account(self,usr): # kullanıcı adı belirlenen property
        self.__username = usr
        return self.__username
    
    def instaAccount(self) -> dict: # Instagram kullanıcısı hakkında bilgi almak için yazılan method
        __header = {
                "User-Agent" : "Instagram 22.0.0.15.68 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-G935F; hero2lte; samsungexynos8890; en_US)",
                "content-type": "application/json; charset=utf-8",
                "x-csrftoken" : self.__readConfig["csrftoken"],
        }
        __response = requests.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.__username}",headers=__header,cookies=self.__readConfig).json()
        # print(__response)
        self.__followeed = __response["data"]["user"]["edge_followed_by"]["count"]
        self.__follow = __response["data"]["user"]["edge_follow"]["count"]
        self.__userID = __response["data"]["user"]["id"]
        return {
                "info":{
                        "follow":__response["data"]["user"]["edge_follow"]["count"],
                        "followeed" : __response["data"]["user"]["edge_followed_by"]["count"],
                        "user_id" : __response["data"]["user"]["id"],
                        "bio" : 'NaN' # eğer ifade boş bir liste döndürürse "NaN" döndürmezse ifadenin kendisini yazdır
                                    if __response["data"]["user"]["biography"] == ''
                                    else __response["data"]["user"]["biography"],

                        "thumbnail":'NaN' # eğer ifade boş bir liste döndürürse "NaN" döndürmezse ifadenin kendisini yazdır
                                        if __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"] == []
                                        else 'https://'+LinkParser(URL_Shortened(__response["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"])).parse,

                        "first_post_id" :'NaN' # eğer ifade boş bir liste döndürürse "NaN" döndürmezse ifadenin kendisini yazdır
                                            if __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"] == []
                                            else __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["id"],
                        "profile_picture" : "https://"+LinkParser(URL_Shortened(__response["data"]["user"]["profile_pic_url_hd"])).parse,
                        "is_follow_me" : "YES" if __response["data"]["user"]["follows_viewer"] else "NO"
                      }
               }

    def readNewDMessages(self): # İlk sıradaki DM mesajlarını okuduğumuz method
        __header = {
            "User-Agent" : "Instagram 22.0.0.15.68 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-G935F; hero2lte; samsungexynos8890; en_US)",
            "content-type": "application/json; charset=utf-8",
            "x-csrftoken" : self.__readConfig["csrftoken"],
        }
        __response = requests.get("https://i.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=10&thread_message_limit=10",
                                  cookies=self.__readConfig,
                                  headers=__header).json()
        __text = ""
        __items = __response["inbox"]["threads"][0]["items"][0]
        for i in __items.values():
            if i == "media_share":
                __text = "https://"+LinkParser(URL_Shortened("https://www.instagram.com/p/"+__items[i]["code"])).parse
            elif i == "text":
                __text = __items["text"]
            
        __sender = __response["inbox"]["threads"][0]["users"][0]["username"]
        __time = str(__items["timestamp"])
        return {
                "info":{
                        "sender":__sender,
                        "msg":__text,
                        "time": str(datetime.fromtimestamp(float(__time[:10]+'.'+__time[10:])))
                      }
               }