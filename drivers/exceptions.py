class InvalidDriverError(Exception):

    def __init__(self, message) -> None:
        self.message = message

class NotRunningError(Exception):

    def __init__(self) -> None:
        self.message = "The requested container is not running !"
