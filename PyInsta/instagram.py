import os
import requests
import json
from datetime import datetime
from fake_useragent import UserAgent
from configparser import ConfigParser
from .utils import(URL_Shortened,LinkParser)
from getpass import getuser
from dotenv import dotenv_values

__accountinfo__ = f"C:\\Users\\{getuser()}\\Documents\\PyInsta"
class Instagram:
    def __init__(self,username:str=...,password:str=...) -> None:
        self.__username = username
        self.__password = password
        self.__cookies = None
        self.loginState = True
        self.__followeed = 0
        self.__cfg = ConfigParser()
        if not os.path.exists(f"{__accountinfo__}\\account.ini") and not os.path.exists(f"{__accountinfo__}\\.env"):
            __response = requests.get("https://www.instagram.com/accounts/login/")
            self.__cookies = __response.cookies.get_dict()
            __loginR = self.__login
            if self.loginState:
                os.system("cls")
                os.mkdir(__accountinfo__)
                with open(f"{__accountinfo__}\\.env","w",encoding="utf-8") as env:
                    with open(f"{__accountinfo__}\\account.ini","w",encoding="utf-8") as ini_file:
                        self.__cfg["ACCOUNT"] = __loginR[0]
                        self.__cfg.write(ini_file)
                        env.write(f"SESSION_ID={__loginR[1]['sessionid']}")

    @property
    def __login(self) -> dict:
        __data = {
            'username' : self.__username,
            'enc_password' : f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{self.__password}',
            'queryParams' : {},
            'optIntoOneTap' : 'false'
        }
        __header = {
            "User-Agent" : UserAgent().random,
            "X-Requested-With" : "XMLHttpRequest",
            "Referer" : "https://www.instagram.com/accounts/login/",
            "x-csrftoken" : self.__cookies["csrftoken"]
        }
        __response = requests.post("https://www.instagram.com/accounts/login/ajax/",data=__data,headers=__header)
        __json_data = json.loads(__response.text)

        if __json_data["authenticated"]:
            json_resp = __response.cookies.get_dict()
            return [
                {
                    "username":self.__username,
                    "password":str(self.__password),
                    "csrftoken":json_resp["csrftoken"],
                    "ds_user_id":json_resp["ds_user_id"],
                    "ig_did":json_resp["ig_did"],
                    "mid":json_resp["mid"],
                    "rur":json_resp["rur"]
                },
                {
                    "sessionid":json_resp["sessionid"]
                }
                   ]
        else:
            self.loginState = False

    @property
    def __readConfig(self) -> dict:
        self.__cfg.read(f"{__accountinfo__}\\account.ini",'utf-8')
        return {
                    "csrftoken" : self.__cfg["ACCOUNT"]["csrftoken"],
                    "ds_user_id" : self.__cfg["ACCOUNT"]["ds_user_id"],
                    "ig_did" : self.__cfg["ACCOUNT"]["ig_did"],
                    "mid" : self.__cfg["ACCOUNT"]["mid"],
                    "rur" : self.__cfg["ACCOUNT"]["rur"],
                    "sessionid" : dotenv_values(f"{__accountinfo__}\\.env")["SESSION_ID"]
               }
    @property
    def which_account(self):
        return self.__username
    
    @which_account.setter
    def which_account(self,usr):
        self.__username = usr
        return self.__username
    
    def instaAccount(self) -> dict:
        __header = {
                "User-Agent" : "Instagram 22.0.0.15.68 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-G935F; hero2lte; samsungexynos8890; en_US)",
                "content-type": "application/json; charset=utf-8",
                "x-csrftoken" : self.__readConfig["csrftoken"],
        }
        __cookies = {
                "csrftoken" : self.__readConfig["csrftoken"],
                "ds_user_id" : self.__readConfig["ds_user_id"],
                "ig_did" : self.__readConfig["ig_did"],
                "mid" : self.__readConfig["mid"],
                "rur" : self.__readConfig["rur"],
                "sessionid" : self.__readConfig["sessionid"]
        }
        __response = requests.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.__username}",headers=__header,cookies=__cookies).json()
        self.__followeed = __response["data"]["user"]["edge_followed_by"]["count"]
        return {
                "info":{
                        "follow":__response["data"]["user"]["edge_follow"]["count"],
                        "followeed" : __response["data"]["user"]["edge_followed_by"]["count"],
                        "user_id" : __response["data"]["user"]["id"],
                        "bio" : 'NaN'
                                    if __response["data"]["user"]["biography"] == ''
                                    else __response["data"]["user"]["biography"],
                        "first_post_owner_comment" :'NaN' 
                                                        if __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"] == [] 
                                                        else __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"],
                        "thumbnail":'NaN'
                                        if __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"] == []
                                        else 'https://'+LinkParser(URL_Shortened(__response["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"])).parse,

                        "first_post_id" :'NaN'
                                            if __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"] == []
                                            else __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["id"]
                      }
               }

    def followAndFollowees(self):
        # QVFBQXg0MmJ5bllEOUlYZGppeWdMVzY3azdQSjJaMkZ0OXBkcnNGd0c5SjFHNktMRGpZM2pqNjZGMGVNTnIyRkpPaUo3TkpGaFpFMkpPbC1ENnI5SmVxSA==
        # QVFEekZkclUxeTY2MnBtazdLeHJFTlNGUU5VWEcxRm5nY3V3RFJvVkJrLUdnNFlRR09hNHU1cnlPbURMN0FOQUIwNld5SjBac3p5cUI0U0FQZnpkT2JNSA==
        data ={
            "count": "12",
            "max_id": "QVFEekZkclUxeTY2MnBtazdLeHJFTlNGUU5VWEcxRm5nY3V3RFJvVkJrLUdnNFlRR09hNHU1cnlPbURMN0FOQUIwNld5SjBac3p5cUI0U0FQZnpkT2JNSA==",
            "search_surface": "follow_list_page"
        }
        header = {
            "User-Agent" : "Instagram 22.0.0.15.68 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-G935F; hero2lte; samsungexynos8890; en_US)",
            "x-csrftoken" : self.__readConfig["csrftoken"],
        }
        cookies = {
            "csrftoken" : self.__readConfig["csrftoken"],
            "ds_user_id" : self.__readConfig["ds_user_id"],
            "ig_did" : self.__readConfig["ig_did"],
            "mid" : self.__readConfig["mid"],
            "rur" : self.__readConfig["rur"],
            "sessionid" : self.__readConfig["sessionid"]
        }
        r = requests.get("https://i.instagram.com/api/v1/friendships/49096008445/followers/?",data=data,params=data,headers=header,cookies=cookies)
        print("{:<10}".format("Takipçiler")+"\n"+"=="*10)
        for i in range(0,self.__followeed):
            response = requests.get("https://i.instagram.com/api/v1/friendships/49096008445/followers/?",data=data,cookies=cookies,headers=header).json()
            print(f"{response['users'][i]['username']:<10}")
            if i == 11:
                data["max_id"] = r.json()["next_max_id"]

    def readNewDMessages(self):
        __header = {
            "User-Agent" : "Instagram 22.0.0.15.68 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-G935F; hero2lte; samsungexynos8890; en_US)",
            "content-type": "application/json; charset=utf-8",
            "x-csrftoken" : self.__readConfig["csrftoken"],
        }
        __cookies = {
            "csrftoken" : self.__readConfig["csrftoken"],
            "ds_user_id" : self.__readConfig["ds_user_id"],
            "ig_did" : self.__readConfig["ig_did"],
            "mid" : self.__readConfig["mid"],
            "rur" : self.__readConfig["rur"],
            "sessionid" : self.__readConfig["sessionid"]
        }
        __response = requests.get("https://i.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=10&thread_message_limit=10",cookies=__cookies,headers=__header).json()
        __text = __response["inbox"]["threads"][0]["last_permanent_item"]["text"]
        __sender = __response["inbox"]["threads"][0]["thread_title"]
        return {
                "info":{
                        "sender":__sender,
                        "msg":__text
                      }
               }