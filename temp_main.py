import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import code
from sklearn.linear_model import LinearRegression as LinReg

data_raw = pd.read_csv('../GlobalTemperatures.csv')

# Look at the initial trend
plt.plot(data_raw['LandAndOceanAverageTemperature'], 'b.')
plt.show()

# Very messy since data is monthly. Need to average by year
time = pd.DatetimeIndex(data_raw['dt'])
years = time.year
year_avg = data_raw.groupby(years).mean()
plt.plot(year_avg['LandAverageTemperature'])
plt.show()

# There is anomaly at 1752. What's up? There are ton of missing values
data_raw[time.year == 1752]
data_raw['LandAverageTemperature'] = data_raw['LandAverageTemperature'].fillna(method='ffill')
print(data_raw.apply(lambda x: sum(x.isnull())))

# Use linear regression to predict the temperature over time
x = year_avg.index.values.reshape(-1, 1)
y = year_avg['LandAverageTemperature']

reg = LinReg()
reg.fit(x,y)
y_preds = reg.predict(x)
print("Accuracy: " + str(reg.score(x,y)))
plt.plot(x, y_preds, 'r-')
plt.plot(year_avg['LandAverageTemperature'], 'b.')
plt.show()
code.interact(local=dict(globals(), **locals()))
