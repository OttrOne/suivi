from .driver import Driver
from .exceptions import InvalidDriver, NotRunning, ImageNotFound
from models.sample import Sample
from typing import Union

import docker

class DockerDriver:

    def __init__(self, raise_errors=True):
        if not issubclass(DockerDriver, Driver):
            raise InvalidDriver(f"{DockerDriver.__name__} is not a valid suivi driver.")

        self.raise_errors = raise_errors
        self._container = None

    def create(self, image: str, command: str):
        self._client = docker.from_env()
        try:
            self._container = self._client.containers.run(image, command, detach=True)
        except docker.errors.ImageNotFound:
            raise ImageNotFound()

        return self._container.id

    def logs(self):
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return

        return self._container.logs()

    def stats(self) -> Union[Sample, None]:
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return

        def calc_cpu_percent(dmp):
            # length indicates the amout of available cpus being used
            print (dmp)

            cpu_count = int(dmp["cpu_stats"]["online_cpus"])
            cpu_percent = 0.0
            cpu_delta = float(dmp["cpu_stats"]["cpu_usage"]["total_usage"]) - float(dmp["precpu_stats"]["cpu_usage"]["total_usage"])
            system_delta = float(dmp["cpu_stats"]["system_cpu_usage"]) - float(dmp["precpu_stats"]["system_cpu_usage"])
            if system_delta > 0.0:
                cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
            return cpu_percent

        tmp = self._container.stats(stream=False)
        return Sample(calc_cpu_percent(tmp), tmp["memory_stats"]["usage"])

    def stop(self):
        if not self._container:
            #if self.raise_errors: raise NotRunning()
            return
        self._container.stop()

    def cleanup(self, volumes=True):
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return
        self._container.remove(v=volumes)

    def __del__(self):
        if self._container:
            self.stop()
            self.cleanup()
