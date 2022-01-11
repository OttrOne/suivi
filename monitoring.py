from drivers.driver import Driver
import time
from threading import Thread

from models import SampleSet

class Monitoring:

    def __init__(self, driver: Driver):
        self.sleep = 1.0
        self._procedure = MonitoringProcedure(driver, self.sleep)

    def stop(self):
        self._procedure.stop()
        self.t.join()

    def start(self):
        if self.sleep != 1.0:
            self._procedure.sleep = self.sleep

        self.t = Thread(target=self._procedure.run)
        self.t.start()

        # wait for metrics to be available
        while True:
            if self._procedure.tracking:
                break
            time.sleep(1)

    def export(self):
        return SampleSet(self._procedure._samples)

class MonitoringProcedure:

    def __init__(self, driver: Driver, sleep) -> None:
        self.driver = driver
        self._running = True
        self._samples = []
        self.sleep = sleep
        self.tracking = False

    def stop(self):
        self._running = False
        self.tracking = False

    def run(self):
         while self._running:
            stats = self.driver.stats()
            if stats:
                self.tracking = True
                self._samples.append(stats)
            elif self.tracking:
                print("metrics not available anymore")
                break
            time.sleep(self.sleep)
