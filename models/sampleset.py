from math import ceil
from utils import hrsize
from . import Sample

class SampleSet:

    round = 3

    def __init__(self, samples) -> None:
        if not (isinstance(samples, list) and all(isinstance(sample, Sample) for sample in samples)):
            raise Exception("samples parameter invalid.")
        self.samples = samples

    def _average(self, samples, rnd=None):

        if rnd:
            return round(sum(samples) / len(samples), rnd)
        return sum(samples) / len(samples)

    def _max(self, samples, rnd=None):

        if rnd:
            return round(max(samples), rnd)
        return max(samples)

    def _percentile(self, samples, perecntile, rnd=0):

        # check borders
        perecntile = 1 if perecntile < 1 else perecntile
        perecntile = 99 if perecntile > 99 else perecntile

        samples.sort()
        index = ((perecntile / 100.0) * len(samples))
        res = -1

        if index % 1 == 0:
            # index not floating point
            index = int(index) # index must be strictly int
            res = 1.0/2 * (samples[index-1] + samples[index])
        else:
            index = ceil(index)
            res = samples[index-1]

        return round(res, rnd)

    def __str__(self) -> str:

        data = self.export()
        return (
            f"CPU (max/avg/80%) {data['cpu']['max']}% / {data['cpu']['average']}% / {data['cpu']['80%']}% \n"
            f"MEM (max/avg/80%) {hrsize(data['memory']['max'])} / {hrsize(data['memory']['average'])} / {hrsize(data['memory']['80%'])}"
        )

    def export(self):

        cpu_samples = [sample.cpupercent for sample in self.samples]
        mem_samples = [sample.memory for sample in self.samples]

        return {
            "cpu" : {
                "max" : self._max(cpu_samples, self.round),
                "80%" : self._percentile(cpu_samples, 80, self.round),
                "average" : self._average(cpu_samples, self.round),
                "samples" : cpu_samples,
            },
            "memory" : {
                "max" : self._max(mem_samples, self.round),
                "80%" : ceil(self._percentile(mem_samples, 80)),
                "average" : ceil(self._average(mem_samples)),
                "samples" : mem_samples,
            },
        }
