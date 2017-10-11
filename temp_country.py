import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import code
from sklearn.linear_model import LinearRegression as LinReg

# Dataset can be found here: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
data_raw = pd.read_csv('../GlobalLandTemperaturesByCountry.csv', encoding = "ISO-8859-1")

# Fill in the missing data
data_raw['AverageTemperature'] = data_raw['AverageTemperature'].fillna(method='ffill')

# I want to convert AverageTemps to Farenheit
data_raw['new_avg_temp'] = data_raw['AverageTemperature']*1.6 + 32
data_raw['new_err_temp'] = data_raw['AverageTemperatureUncertainty']*1.6

# For now, drop all data before 1950:
time = pd.DatetimeIndex(data_raw['dt'])
data_raw['year'] = time.year
data_recent = data_raw.drop(data_raw[data_raw.year < 1950].index)

# Creates plot of historical temperature for given country:
def plotme(places=[]):
    for place in places:
        main = data_raw[data_raw.Country == place]
        time_place = pd.DatetimeIndex(main['dt'])
        country_data = main.groupby(time_place.year).mean()
        plt.plot(country_data['new_avg_temp'])
        plt.suptitle('Temperature History 1750-Present')
        plt.xlabel('Year')
        plt.ylabel('Temp (F)')
        plt.legend(places, loc='upper left')
    plt.show()
whatever = ['France', 'India']
plotme(whatever)

# Predicts the slope(rate of increase) in temperature for a given country
def predictme(place):
    main = data_recent[data_recent.Country == place]
    time_place = pd.DatetimeIndex(main['dt'])
    country_data = main.groupby(time_place.year).mean()
    m, b = np.polyfit(country_data.index, country_data['new_avg_temp'], 1)
    return m
    # print(place + "'s rate of change (F/yr): " + str(m))
print(predictme('France'))

# Determine which country has highest rate of temp increase
temp_changes = dict()
countries = data_recent.Country.unique()

for i in countries[:10]:
    predictme(i)
    temp_changes[i] = predictme(i)

highest_country = max(temp_changes, key = temp_changes.get)
print(highest_country, '(F/yr): ', temp_changes[highest_country])


code.interact(local=dict(globals(), **locals()))
