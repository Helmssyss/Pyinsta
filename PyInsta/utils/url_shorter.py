import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from html.parser import HTMLParser

class URL_Shortened(requests.Session):
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
        self.r = self.post("https://www.shorturl.at/shortener.php",headers=header,data=data)
    
    def linkScrape(self):
        soup = BeautifulSoup(self.r.content,"lxml")
        return str(soup.find("input",attrs={"id":"shortenurl"}))

class LinkParser(HTMLParser):
    def __init__(self,url:URL_Shortened):
        super().__init__()
        self.parse = ""
        self.feed(url.linkScrape())

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            v,l = attr
            if v == "value":
                self.parse += l
                return self.parse