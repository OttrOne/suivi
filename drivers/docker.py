from re import S
from .exceptions import NotRunning, ImageNotFound
from models import Sample, SampleSet
from typing import Union
from utils import id_generator
from docker import from_env, errors as derr
from math import ceil
from time import sleep

class DockerDriver:

    def __init__(self, raise_errors=True):

        self.raise_errors = raise_errors
        self._container = None
        self._network = None
        self._online_cpu = None

    def ready(self):

        return self._container.status == "running"

    def create(self, image: str, command: Union[None, str]):
        self._client = from_env()
        id = id_generator()
        self._network = self._client.networks.create(f"suivi-{id}-net")

        try:
            self._container = self._client.containers.run(
                image,
                command,
                network=self._network.name,
                name=f"suivi-{id}",
                detach=True
            )
            print(self._container.status)
        except derr.ImageNotFound:
            raise ImageNotFound()

        self.hostname = f"suivi-{id}"

        return self._container.id

    def wait(self, name):
        self._companion.wait()

    def logs(self):
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return

        return self._container.logs()

    def stats(self) -> Union[Sample, None]:
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return

        def calc_cpu(dmp):
            # length indicates the amout of available cpus being used
            if "online_cpus" not in dmp["cpu_stats"]:
                return None

            cpu_count = int(dmp["cpu_stats"]["online_cpus"])
            cpu = 0.0
            cpu_delta = float(dmp["cpu_stats"]["cpu_usage"]["total_usage"]) - float(dmp["precpu_stats"]["cpu_usage"]["total_usage"])
            system_delta = float(dmp["cpu_stats"]["system_cpu_usage"]) - float(dmp["precpu_stats"]["system_cpu_usage"])
            if system_delta > 0.0 and cpu_delta > 0.0:
                cpu = (cpu_delta / system_delta) * cpu_count

            return cpu
        tmp = self._container.stats(stream=False)
        if "online_cpus" in tmp["cpu_stats"] and not self._online_cpu:
                self._online_cpu = tmp["cpu_stats"]["online_cpus"]

        cpu = calc_cpu(tmp)
        mem = "usage" in tmp["memory_stats"]

        if cpu and mem:
            return Sample(cpu, int(tmp["memory_stats"]["usage"]))

        return None

    def stop(self):
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return
        self._container.stop()

    def join(self, image: str, command: Union[None, str]):

        try:
            self._companion = self._client.containers.run(
                image,
                command,
                network=self._network.name,
                name=f"{self._container.name}-companion-{id_generator()}",
                detach=True
            )
        except derr.ImageNotFound:
            raise ImageNotFound()

        return self._companion.id

    def cleanup(self, volumes=True):
        if not self._container:
            if self.raise_errors: raise NotRunning()
            return
        self._container.remove(v=volumes)
        self._network.remove()

    def forecast(self, samples: SampleSet) -> str:

        def csize(num: int) -> str:
            for unit in ['b', 'k', 'm', 'g']:
                if num < 1000.0:
                    return f"{ceil(num)}{unit}"
                num /= 1000.0

        samples = samples.export()
        cpu = samples['cpu']['80%']
        mem = samples['memory']['80%']

        # minimum for mem is 6m
        mem = "6m" if mem < 6 * 1024 * 1024 else csize(mem)
        # minimum for cpu is 0.01
        cpu = 0.01 if cpu < 0.01 else cpu

        if self._online_cpu:
            cpu = self._online_cpu if cpu > self._online_cpu else cpu

        return f"--cpus={cpu:2.2f} --memory={mem}"

