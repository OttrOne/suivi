import pmdarima as pm
from pmdarima.model_selection import train_test_split
from pmdarima.arima import ADFTest
import numpy as np
from models import SampleSet
from path import Path
from json import loads
import matplotlib.pyplot as plt

class Forecaster:

    def __init__(self, data: SampleSet, config={}) -> None:
        self._config = config
        self._data = data

    def run_arima(self):

