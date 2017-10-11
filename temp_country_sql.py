import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import code
import psycopg2

# Dataset can be found here: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
conn_string = "host='localhost' dbname='Climate_data' user='postgres' password='postgres'"
print("Connecting to database", conn_string)
conn = psycopg2.connect(conn_string)
# conn.cursor will return a cursor object, you can use this cursor to perform queries.

cursor = conn.cursor()
cursor.execute("SELECT * FROM country WHERE LOWER(country) IN('india', 'germany', 'brazil', 'canada', 'australia', 'kenya', 'greece')")
sql_data = cursor.fetchall()

cursor.close()
conn.close()

# Put the data into a new dataframe and fill missing data
data_raw = pd.DataFrame(sql_data)
data_raw.columns = ['date', 'avg_temp', 'error_temp', 'country']

data_raw['avg_temp'] = data_raw['avg_temp'].fillna(method='ffill')
data_raw['error_temp'] = data_raw['error_temp'].fillna(method='ffill')

# I want to convert AverageTemps to Farenheit
data_raw['new_avg_temp(F)'] = data_raw['avg_temp'].apply(lambda x: float(x)*1.6 + 32)
data_raw['new_error_temp(F)'] = data_raw['error_temp'].apply(lambda x: float(x)*1.6)


# Creates plot of historical temperature for given country:
def plotme(place):
    place = place.lower()
    main = data_raw[data_raw.country.str.lower() == place]
    time_place = pd.DatetimeIndex(main['date'])
    country_data = main.groupby(time_place.year).mean()
    plt.plot(country_data['new_avg_temp'])
    plt.suptitle('Temperature History for ' + place)
    plt.xlabel('Year')
    plt.ylabel('Temp (F)')
    plt.show()

plotme('India')

# Focus on period after oil/coal usage really shot up: drop all data before 1950
time = pd.DatetimeIndex(data_raw['date'])
data_raw['year'] = time.year
data_recent = data_raw.drop(data_raw[data_raw.year < 1950].index)

# Predicts the slope(rate of increase) in temperature for a given country
def predictme(place):
    place = place.lower()
    main = data_recent[data_recent.country.str.lower() == place]
    time_place = pd.DatetimeIndex(main['date'])
    country_data = main.groupby(time_place.year).mean()
    m, b = np.polyfit(country_data.index, country_data['new_avg_temp'], 1)
    return m
    # print(place + "'s rate of change (F/yr): " + str(m))
print(predictme('India'))

# Determine which country has highest rate of temp increase
temp_changes = dict()
countries = data_recent.country.unique()
for i in countries[:10]:
    predictme(i)
    temp_changes[i] = predictme(i)

highest_country = max(temp_changes, key = temp_changes.get)
print(highest_country, '(F/yr): ', temp_changes[highest_country])


code.interact(local=dict(globals(), **locals()))
