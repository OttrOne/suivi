
class Sample:

    cpupercent : float
    memory: int

    def __init__(self, cpu, mem) -> None:
        self.cpupercent = cpu
        self.memory = mem

class SampleSet:

    round = 3

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
