from drivers.driver import Driver
from time import sleep
from utils import handle_variables

class Penetration:

    def __init__(self, driver: Driver, config={}) -> None:
        self._config = config
        self._client = driver

        #TODO there should not be a companion with no image...
        self.image = config.get('image', None)
        self.command = config.get('cmd', None)

    def penetrate(self):

        companion = self._client.join(self.image, self.command)
        self._client.wait(companion)

