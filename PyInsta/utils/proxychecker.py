from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from typing import Generator
from bs4 import BeautifulSoup
from colorama import init,Fore
import requests

init(autoreset=True)
class ProxyChecker:
    def __init__(self,prxtype:str=...,isProxyPath:bool=False,filePath:str=...) -> None:
        self.__prxtype = prxtype
        self.__isProxyPath = isProxyPath
        self.__filePath = filePath
        self.__url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={self.__prxtype}&timeout=10000&country=all&ssl=all&anonymity=all"
        self.__allproxy = None
        self.__worker = []

        if not self.__isProxyPath:
            for prxies in list(self.__scrap):
                self.__allproxy = prxies.split("|")
            self.__allproxy.remove('')
            self.__isWorkerProxy()
        else:
            try:
                print(f"{Fore.YELLOW}[{self.__filePath}]  ─────  Reading Proxy file")
                sleep(2)
                with open(self.__filePath,"r") as prxfile:
                    self.__allproxy =prxfile.readlines()
                    for prx in range(len(self.__allproxy)):
                        self.__allproxy[prx] = self.__allproxy[prx].replace("\n","")
                    self.__isWorkerProxy()
            except FileNotFoundError:
                print(f"{Fore.RED}Please Specify the Path of the Proxy File{Fore.RESET}")

    @property
    def __scrap(self) -> Generator[str,str,str]:
        with requests.Session() as session:
            soup = BeautifulSoup(session.get(url=self.__url).content,"lxml")
            for i in soup.find_all("p"):
                yield i.text.replace("\r\n","|")

    def __checkedProxy(self,timeout:int,proxy:str):
        p = {}
        if not self.__isProxyPath:
            p = {"http":f"{self.__prxtype}://"+proxy,"https":f"{self.__prxtype}://"+proxy}
        else:
            p = {"http":f"http://"+proxy,"https":f"http://"+proxy}
        
        with requests.Session() as session:
            session.get("https://httpbin.org/ip",timeout=timeout,proxies=p)

    def __isWorkerProxy(self):
        with ThreadPoolExecutor(max_workers=len(self.__allproxy)) as ex:
            future_to_proxy = {ex.submit(self.__checkedProxy,30,prx):prx for prx in self.__allproxy}
            for future in as_completed(future_to_proxy):
                value = future_to_proxy[future]
                try:
                    future.result()
                except:
                    print(f"{Fore.RED}UNSUCCESSFUL : {value}{Fore.RESET}")
                else:
                    print(f"{Fore.GREEN}SUCCESSFUL   : {value}{Fore.RESET}")
                    self.__worker.append(value)
    @property
    def getWorkerProxy(self) -> list[str]:
        return list(set(self.__worker))