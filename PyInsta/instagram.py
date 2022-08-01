import os
import requests
import json
from datetime import datetime
from fake_useragent import UserAgent # user-agent sınıfı
from configparser import ConfigParser
from .utils import(URL_Shortened,LinkParser) # Kişinin paylaştığı en güncel post bir resim linki barındırıyor. O linke buradan ulaşıp linki kısaltan sınıfları
                                             # ekliyorum
from getpass import getuser # Bilgisayar adı kişiden kişiye değiştiği için gerekli gördüğüm fonksiyon
from dotenv import dotenv_values # ".env" dosyasındaki "key=value" biçeminde yazılan ifadede "value"'a ulaşabilmek için bu fonksiyonu dahil ediyorum

__accountinfo__ = f"C:\\Users\\{getuser()}\\Documents\\PyInsta" # "Belgelerim" klasörüne "PyInsta" adında klasör oluşturmak için verdiğim yol
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
        if not os.path.exists(f"{__accountinfo__}\\account.ini") and not os.path.exists(f"{__accountinfo__}\\.env"):
            # "account.ini" ve ".env" yok ise
            __response = requests.get("https://www.instagram.com/accounts/login/") # login sayfasına gidilir
            self.__cookies = __response.cookies.get_dict() # gidilen sayfadan cookieler çekilir
            __loginR = self.__login # cookieler çekildikten sonra instagram kullanıcı adı ve parola ile giriş işlemi gerçekleştirilir
            if self.loginState: # giriş işlemi başarılı ise
                os.system("cls") # Terminal ekranını temizler
                os.mkdir(__accountinfo__) # belirlenen yolda belgelerimin içine Pyinsta adında bir klasör oluşturur
                with open(f"{__accountinfo__}\\.env","w",encoding="utf-8") as env:
                    with open(f"{__accountinfo__}\\account.ini","w",encoding="utf-8") as ini_file:
                        self.__cfg["ACCOUNT"] = __loginR[0] # döndürülen listedeki ilk sözlük verisini yazdırıyorum
                        self.__cfg.write(ini_file) # klasör içerisine ".ini" dosyası yazılır
                        env.write(f"SESSION_ID={__loginR[1]['sessionid']}") # klasör içerisine ".env" dosyası yazılır
                                                                            # klasör içerisine döndürülen listedeki ikinci sözlük verisini yazdırıyorum
    @property
    def __login(self) -> dict: # giriş işlemi
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
            "x-csrftoken" : self.__cookies["csrftoken"]
        }
        __response = requests.post("https://www.instagram.com/accounts/login/ajax/",data=__data,headers=__header) # ilgili linke post işlemi yapıyorum
        __json_data = json.loads(__response.text) # json formatına çeviriyorum
        if __json_data["authenticated"]: # belirlenen anahtar ve belirlenen anahtarın değeri True ise
            json_resp = __response.cookies.get_dict() # cookieleri çekiyorum
            return [ # çekilen cookieleri bir liste içerisinde sözlük kullanarak döndürüyorum
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
        else: # giriş başarısız olursa yani belirlenen anahtar yok ise
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
                        "first_post_owner_comment" :'NaN' # eğer ifade boş bir liste döndürürse "NaN" döndürmezse ifadenin kendisini yazdır
                                                        if __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"] == [] 
                                                        else __response["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"],
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
        __response = requests.get("https://i.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=10&thread_message_limit=10",cookies=self.__readConfig,headers=__header).json()
        __text = __response["inbox"]["threads"][0]["last_permanent_item"]["text"] #if not __response["inbox"]["threads"][0]["items"][0]["media_share"]["code"] else "Sent Video\n\t\t   ╰──────≻ "+"https://"+LinkParser(URL_Shortened("https://instagram.com/p/"+__response["inbox"]["threads"][0]["items"][0]["media_share"]["code"])).parse
        __sender = __response["inbox"]["threads"][0]["thread_title"]
        __time = str(__response["inbox"]["threads"][0]["items"][0]["timestamp"])
        return {
                "info":{
                        "sender":__sender,
                        "msg":__text,
                        "time": str(datetime.fromtimestamp(float(__time[:10]+'.'+__time[10:]))) # timestamp türünde olan veriyi önce stringe çevirip ardından
                                                                                                # float veri tipine dönüştürüyorum.
                      }
               }