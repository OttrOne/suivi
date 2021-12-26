from docker.models.containers import Container
from .driver import Driver
from .exceptions import InvalidDriverError
from models.sample import SampleSet, Sample
from monitoring import Monitoring

import docker
import asyncio
import queue
import threading

q = queue.Queue()

def getSamples(container: Container, q):
    def calculate_cpu_percent(d):
        # length indicates the amout of available cpus being used
        cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
        cpu_percent = 0.0
        cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - float(d["precpu_stats"]["cpu_usage"]["total_usage"])
        system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - float(d["precpu_stats"]["system_cpu_usage"])
        if system_delta > 0.0:
            cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
        return cpu_percent

    while True:
        tmp = container.stats(stream=False)
        q.put(Sample(calculate_cpu_percent(tmp), tmp["memory_stats"]["usage"]))

async def sampleStats(container: Container, samples):

    def calculate_cpu_percent(d):
        # length indicates the amout of available cpus being used
        cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
        cpu_percent = 0.0
        cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - float(d["precpu_stats"]["cpu_usage"]["total_usage"])
        system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - float(d["precpu_stats"]["system_cpu_usage"])
        if system_delta > 0.0:
            cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
        return cpu_percent

    sampleslst=[]
    stats=[]
    for i in range(0,samples):
        tmp = container.stats(stream=False)
        sampleslst.append(Sample(calculate_cpu_percent(tmp), tmp["memory_stats"]["usage"]))
        stats.append(tmp)
        print(f"Sample {i+1}/{samples}")
        await asyncio.sleep(0.2)

    return SampleSet(sampleslst)

class DockerDriver:

    def __init__(self):
        if not issubclass(DockerDriver, Driver):
            raise InvalidDriverError(f"{DockerDriver.__name__} is not a valid suivi driver.")

        self.loop = asyncio.get_event_loop()

    def create(self):
        self.client = docker.from_env()
        self.container = self.client.containers.run("ubuntu:latest", "tail -f /dev/null", detach=True)

    def logs(self):
        if not self.container:
            print("Container not running.")
            return

        print(self.container.logs())

    def mon_start(self):
        self.loop.run_forever()

    def mon_end(self):
        pass

    def stats(self, samples=10):
        if not self.container:
            print("Container not running.")
            return
        def calculate_cpu_percent(d):
            # length indicates the amout of available cpus being used
            cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
            cpu_percent = 0.0
            cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - float(d["precpu_stats"]["cpu_usage"]["total_usage"])
            system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - float(d["precpu_stats"]["system_cpu_usage"])
            if system_delta > 0.0:
                cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
            return cpu_percent

        tmp = self.container.stats(stream=False)
        return Sample(calculate_cpu_percent(tmp), tmp["memory_stats"]["usage"])
        #t1 = threading.Thread(target=getSamples, name=getSamples, args=(self.container, q,))
        #t1.start()
        #while True:
        #    value = q.get()
        #    print(value.cpupercent)
        #smplset = asyncio.run(sampleStats(self.container, samples))
        #return smplset.export()

    def stop(self):
        if not self.container:
            print("Container not running.")
            return

        self.container.stop()
        print("Container stopped.")

    def __del__(self):
        self.stop()
