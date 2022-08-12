import sys
import os
from time import sleep
from Pydate import PyDate
from .utils import Console

__version__ = 0.1
version_link = "https://raw.githubusercontent.com/Arif-Helmsys/Pyinsta/main/version.json"
class Control(PyDate):
    def __init__(self, path: str, version_raw_link="") -> None:
        super().__init__(path, version_raw_link, isScript = True)
        if not os.path.exists(f"{os.getcwd()}\\version.json"):
            self.createVersionFile(version=__version__)

        if not self.isUpdate:
            while True:
                _input_ = input(f"{Console.COMMAND_LINE}~ [New Update Available]-(Y/n) ")
                if _input_.lower() == "y":
                    self.saveNewVersion(False)
                    self.scriptUpdate(script_raw_link="https://raw.githubusercontent.com/Arif-Helmsys/Pyinsta/main/app.py")
                    print("UPDATED!")
                    sleep(1)
                    print("Restart the Pyinsta")
                    sys.exit(0)

                elif _input_.lower() == "n":
                    print("Please Updated!")

    def scriptUpdate(self, script_raw_link: str) -> bool:
        return super().scriptUpdate(script_raw_link, myscript="app")

    def createVersionFile(self, version: float) -> bool:
        return super().createVersionFile(version)

if __name__ != "__main__":
    ctrl = Control(path=os.getcwd(),version_raw_link=version_link)
