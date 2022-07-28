from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Generator
from bs4 import BeautifulSoup
import requests

class ProxyChecker:
    def __init__(self) -> None:
        self.__url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all"
        self.__allproxy = None
        self.__worker = []
        for prxies in list(self.__scrap):
            self.__allproxy = prxies.split("|")
        self.__allproxy.remove('')

    @property
    def __scrap(self) -> Generator[str,str,str]:
        with requests.Session() as session:
            soup = BeautifulSoup(session.get(url=self.__url).content,"lxml")
            for i in soup.find_all("p"):
                yield i.text.replace("\r\n","|")

    def __checkedProxy(self,timeout:int,proxy:str):
        with requests.Session() as session:
            p = {"https":"http://"+proxy,"http":"http://"+proxy}
            session.get("https://httpbin.org/ip",timeout=timeout,proxies=p)

    def threadEX(self):
        with ThreadPoolExecutor(max_workers=len(self.__allproxy)) as ex:
            future_to_proxy = {ex.submit(self.__checkedProxy,30,prx):prx for prx in self.__allproxy}
            for future in as_completed(future_to_proxy):
                value = future_to_proxy[future]
                try:
                    future.result()
                except:
                    print(f"UNSUCCESSFUL : {value}")
                else:
                    print(f"SUCCESSFUL   : {value}")
                    self.__worker.append(value)
    @property
    def getWorkerProxy(self) -> list[str]:
        return list(set(self.__worker))

p = ProxyChecker()
p.threadEX()
print(p.getWorkerProxy)