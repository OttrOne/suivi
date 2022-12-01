import matplotlib.pyplot as plt
import numpy as np
from path import Path
from json import loads

import pmdarima as pm
from pmdarima.model_selection import train_test_split
from pmdarima.arima import ADFTest

data = loads(Path('export-ba.json').text())
plt.figure()
plt.subplot(211)
ypoints = np.array(data['cpu']['samples'])
xpoints = np.array(range(len(ypoints)))
plt.plot(xpoints, ypoints, 'bo', xpoints, ypoints, 'k')
plt.axhline(y=data['cpu']['80%'], color='r', linestyle='-.', label ='80th percentile')
plt.axhline(y=data['cpu']['average'], color='g', linestyle=':', label ='arithm average')
plt.ylabel('CPU Utilization in %')
plt.legend()

ax = plt.subplot(212)
ypoints = np.array(data['memory']['samples'])
xpoints = np.array(range(len(ypoints)))
plt.plot(xpoints, ypoints, 'bo', xpoints, ypoints, 'k')
plt.axhline(y=data['memory']['80%'], color='r', linestyle='-.', label ='80th percentile')
plt.axhline(y=data['memory']['average'], color='g', linestyle=':', label ='arithm average')
plt.xlabel('Measuring points')
plt.ylabel('Memory Utilization [Bytes]')
txt="Figure 1 - Darstellung der Messwerte eines NGINX Container Lasttests mit Apache Benchmark"
plt.figtext(0.5, 0.01, txt, horizontalalignment='center', fontsize=12)
plt.legend()
plt.show()
