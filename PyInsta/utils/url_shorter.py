# Author: Helmsys

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from html.parser import HTMLParser # html ifadesini parse etmek için(ayrıştırmak için) bu sınıfı dahil ediyorum

class URL_Shortened(requests.Session): # aldığı url sonucunda kısaltılmış linki saklayan html ifadesine erişen sınıf
    def __init__(self,url) -> None:
        super().__init__()
        data = {
            "u": url
        }
        header = {
            "user-agent": UserAgent().random,
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.shorturl.at",
            "referer": "https://www.shorturl.at/"
        }
        self.r = self.post("https://www.shorturl.at/shortener.php",headers=header,data=data) # link kısaltma işlemini yapıyor
    
    def linkScrape(self): # kısaltma işleminden sonra "input" etiketine sahip bir html ifadesi "value" adında bir ifadeye sahip. bu valueye karşılık kısa
                          # linki barındırıyor.
        soup = BeautifulSoup(self.r.content,"lxml")
        return str(soup.find("input",attrs={"id":"shortenurl"})) # input etiketini döndürüyorum

class LinkParser(HTMLParser): # input etiketi parse etmek için sınıf tanımlıyorum
    def __init__(self,url:URL_Shortened): # üstteki sınıfı parametre olarak alıyorum
        super().__init__()
        self.parse = "" # parse edilecek veriyi saklayacak değişkeni tanımlıyorum
        self.feed(url.linkScrape()) # input etiketini gönderiyorum

    def handle_starttag(self, tag, attrs): # input etiketindeki value değerine karşılık gelen kısaltılmış linke ulaşmak için burada parse ediyorum
        for attr in attrs:
            v,l = attr
            if v == "value":
                self.parse += l
                return self.parse # parse edilmiş veriyi döndürüyorum
