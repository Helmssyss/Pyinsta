import requests

class MultiAccount(requests.Session):
    def __init__(self) -> None:
        super().__init__()

MultiAccount()
# to be continued....