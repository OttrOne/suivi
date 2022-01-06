
def hrsize(num: int) -> str:
    for unit in ['', 'KiB', 'MiB', 'GiB', 'TiB']:
        if num < 1024.0:
            return f"{num:3.1f}{unit}"
        num /= 1024.0

class Sample:

    cpupercent : float
    memory: int
    round: int = 5

    def __init__(self, cpu, mem) -> None:
        self.cpupercent = cpu
        self.memory = mem

    def __str__(self) -> str:
        return f"CPU: {round(self.cpupercent,self.round)}%, MEM: {hrsize(self.memory)}"

class SampleSet:

    round = 5

    def __init__(self, samples) -> None:
        if not (isinstance(samples, list) and all(isinstance(sample, Sample) for sample in samples)):
            raise Exception("samples parameter invalid.")
        self.samples = samples

    def export(self):

        return {
            "cpu" : {
                "average" : round(sum([sample.cpupercent for sample in self.samples]) / len(self.samples), self.round),
                "samples" : [sample.cpupercent for sample in self.samples],
            },
            "memory" : {
                "average" : sum([sample.memory for sample in self.samples]) / len(self.samples),
                "samples" : [sample.memory for sample in self.samples],
            },
        }
