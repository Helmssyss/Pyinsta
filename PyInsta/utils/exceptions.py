class BlockedIP(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class WrongPassword(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DeadProxy(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FuckedLogin(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)