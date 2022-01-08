from .driver import Driver
from .exceptions import InvalidDriver, NotRunning, ImageNotFound
import kubernetes

class KubernetesDriver:

    def __init__(self, raise_errors=True):

        self.raise_errors = raise_errors
        self._container = None
        kubernetes.kubernetes.config.load_kube_config()

    def create(self,a,b):
        pass

    def logs(self):
        pass

    def stats(self):
        pass

    def stop(self):
        pass

    def cleanup(self):
        pass
