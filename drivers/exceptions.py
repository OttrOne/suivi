class DriverBaseException(Exception):

    def __init__(self, message) -> None:
        self.message = message

    def __str__(self):
        return f"{self.message}"

class InvalidDriver(DriverBaseException):
    pass

class NotRunning(DriverBaseException):

    def __init__(self) -> None:
        self.message = "The requested container is not running !"

class DriverNotFound(DriverBaseException):

    def __init__(self) -> None:
        self.message = "The requested driver could not be found !"

class ImageNotFound(DriverBaseException):

    def __init__(self) -> None:
        self.message = "The requested image could not be found !"
