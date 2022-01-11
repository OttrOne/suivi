from strictyaml.scalar import Datetime
from utils import hrsize
from time import time_ns

class Sample:

    cpupercent : float
    memory: int
    round: int = 3

    def __init__(self, cpu: int, mem: int) -> None:
        self.cpupercent = cpu
        self.memory = mem
        self.timestamp = time_ns()

    def __str__(self) -> str:
        return f"CPU: {round(self.cpupercent,self.round)}%, MEM: {hrsize(self.memory)}"
