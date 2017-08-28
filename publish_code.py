import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import scipy.interpolate
import scipy.stats as sp
import code

matches = pd.read_csv('2017-Real.csv')

# Determine the probability of winning based on the disparity in the rankings
ranks = matches.LRank - matches.WRank
loser_ranks = matches.WRank = matches.LRank
ranks_new = ranks[np.abs(ranks - np.mean(ranks))<=(1.5*np.std(ranks))]

values, base = np.histogram(ranks_new, bins=100)
bin_prob=values/len(ranks_new)
cumulative_prob = np.cumsum(bin_prob)
plt.plot(base[:-1], cumulative_prob, c='blue')

def predict_winner(x):
    if x < base.min():
        print("The probability of a win is likely 0%")
    elif x > base.max():
        print("The probability of a win is likely 100%")
    else:
        y_interp = scipy.interpolate.interp1d(base[:-1], cumulative_prob)
        y_for = (y_interp(x))
        y_against = (y_interp(-x))
        y_prob = (y_for)/(y_for + y_against)
        print("Probabilty of winning", x, "is:", y_prob)
predict_winner(-2502)
predict_winner(-50)
predict_winner(-5)
predict_winner(0)
predict_winner(10)
predict_winner(15)
predict_winner(60)
predict_winner(130)

# Use this data to predict the 1st round winners of the Wimbledon Grand Slam
# Determine the probability of winning after taking the 1st set


# Determine the probability of beating one of the big four

# Determine if there is a correlation between country and playing surface
