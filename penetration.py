from drivers.driver import Driver
from time import sleep
from utils import handle_variables

class Penetration:

    def __init__(self, driver: Driver, config=None) -> None:
        self._config = config
        self._client = driver
        self._parse_config()

    def _parse_config(self):

        self.image = None
        self.command = None

        if not self._config:
            return

        if 'image' in self._config:
            self.image = self._config['image']

        if 'cmd' in self._config:
            self.command = self._config['cmd']




    def penetrate(self):

        context = {
            'HOST': self._client._container.name,
        }

        #self.command = [handle_variables(command, context) for command in self.command]
        self._client.join(self.image, handle_variables(self.command, context))
        self._client._companion.wait()
        # print(self._client._companion.logs())

