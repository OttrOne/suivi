from utils import hrsize

class Sample:

    cpupercent : float
    memory: int
    round: int = 3

    def __init__(self, cpu, mem) -> None:
        self.cpupercent = cpu
        self.memory = mem

    def __str__(self) -> str:
        return f"CPU: {round(self.cpupercent,self.round)}%, MEM: {hrsize(self.memory)}"
