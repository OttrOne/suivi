from strictyaml.scalar import Datetime
from utils import hrsize
from time import time_ns

class Sample:

    cpu : float
    memory: int
    round: int = 5

    def __init__(self, cpu: int, mem: int) -> None:
        self.cpu = cpu
        self.memory = mem
        self.timestamp = time_ns()

    def __str__(self) -> str:
        return f"CPU: {round(self.cpu * 100.0,self.round)}%, MEM: {hrsize(self.memory)}"
