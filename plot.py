import matplotlib.pyplot as plt
import numpy as np
from math import ceil
from path import Path
from json import loads

import pmdarima as pm
from pmdarima.model_selection import train_test_split
from pmdarima.arima import ADFTest

data = loads(Path('export-ba.json').text())

def _percentile(samples, perecntile, rnd=0):

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

print("eee")
#ypoints = np.array(data['memory']['samples'])
ypoints = np.array(data['cpu']['samples'])
xpoints = np.array(range(len(ypoints)))
arr = np.array( [ypoints, xpoints])

train_size = int(np.ceil(len(ypoints) * 0.75))
train, test = train_test_split(ypoints, train_size=train_size)

model = pm.auto_arima(train, m=1, saisonal=False)

forecasts_size = int(np.ceil(train_size / 2))

forecasts = model.predict(forecasts_size)

#print(train)
#print(forecasts)
#print(train.tolist() + forecasts.tolist())
samples = train.tolist() + forecasts.tolist()

#samples = ypoints.tolist()
percentile = _percentile(samples, 90, 5)
print(percentile)
x = np.arange(train_size + forecasts_size)

#plt.ylabel('Memory Utilization [Bytes]')

plt.ylabel('CPU Utilization in Cores')
plt.xlabel('Measuring points')

#plt.plot(x[:train_size], train, c='blue')
#plt.plot(x[train_size:], forecasts, c='green', label ='ARIMA forecast')
plt.plot(xpoints, ypoints, c='black', label ='measured utilization')
plt.axhline(y=percentile, color='r', linestyle='dotted', label ='90th percentile')
plt.legend()
plt.show()
