from Pydate import PyDate

class Control(PyDate):
    def __init__(self, path: str, version_raw_link="", isScript=False) -> None:
        super().__init__(path, version_raw_link, isScript)

# to be continued....