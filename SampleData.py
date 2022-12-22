#source: the code to generate synthetic time series data below was fetched from RobustSTL code repository 
#the commented lines in the functions are some of the methods i tried out to extract different samples and since it gives 
#multiple or complex seasonality which cannot be handled by STL, just proceeding with the method used by RobustSTL authors

#the sample generator gives trend, seasonal, remainder+anomaly and the sum of trend+seasonal+remainder i.e. the sample data 

#dependencies 

import numpy as np
from numpy import random 
import pandas as pd 
import matplotlib.pyplot as plt 

def season_generator(total_len, seas_len, level):
    seasons = np.zeros([seas_len])
    # random_val = 2.0 * (random.random(seas_len) - 1.5)
    # seasons = np.tile(random_val, total_len)[:total_len]
    seas_idx = int(seas_len / 2)
    seasons[:seas_idx] += level
    seasons[seas_idx:] -= level
    seasons = np.tile(seasons, total_len)[:total_len]
    return seasons

def trend_generator(total_len, level, total_change_points):
    change_points = np.random.choice(total_len, total_change_points, replace = False)
    # trend = np.random.random(total_len)#.cumsum()
    trend = np.zeros([total_len])
    for val in change_points:
        # if (np.random.choice([-1, 1]) == -1):
        #     trend[val: ] -= np.random.choice([-level, level])
        # else:
        trend[val: ] += np.random.choice([-1, 1]) * level
    return trend 

def remainder_generator(total_len, std, mean):
    remainder = np.random.normal(mean, std, (total_len,))
    return remainder

def anomaly_generator(total_len, anomaly_num, level):
    time_steps = np.random.choice(total_len, anomaly_num)
    anomaly = np.zeros([total_len])
    for val in time_steps:
        anomaly[val] += np.random.choice([-1, 1]) * level
    return anomaly


def sample_generator(total_len = 750
                    , trend_change_points = 12
                    , trend_level = 4
                    , seas_len = 50
                    , seas_level = 2
                    , anomaly_num = 7
                    , anomaly_level = 4
                    , noise_mean = 0
                    , noise_std = 0.1486):

    assert total_len >= seas_len
    seasons = season_generator(total_len, seas_len = seas_len, level = seas_level)
    trends = trend_generator(total_len, level = trend_level, total_change_points = trend_change_points)
    remainders = remainder_generator(total_len, std = noise_std, mean = noise_mean)
    anomalies = anomaly_generator(total_len, anomaly_num, level = anomaly_level)
    sample = seasons + trends + remainders + anomalies
    return [sample, trends, seasons, remainders + anomalies]



# sample, trend, season, _ =  sample_generator()

