#================================================================================================================================
#the parameters used in the below code are picked up based on the structure of underlying data - also used plot_seasonal function 
#from R to better understand the seasonal window (loess smoothing window for cyclic subseries) 
#STL paper gives a detailed explanation of choosing the parameter values 
#for the sample data generated, seasonal = 11, trend = 91, low_pass = 51 provided good accuracy - but still this can be optimized 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import SampleData
from statsmodels.tsa.seasonal import STL
obs_sample, obs_trend, obs_season, _ = SampleData.sample_generator()
sample_ts = pd.Series(obs_sample)
stl = STL(sample_ts, period = 50, trend = 91, low_pass = 51, seasonal = 15, robust = True)
res = stl.fit()



#the below method to find the trend and low pass combination might not be the best way to get these values 
#but i just tried out to see if the values from this can yield more accuracy - (the parameter i have chosen initially gave better 
#accuracy)

trend = np.array([t for t in np.arange(51, 85, 1) if t%2 !=0])
low_pass = trend.copy()



mae_t = [] #mae for trend
mse_t = [] #mse for trend
mae_s = [] #mae for season
mse_s = [] #mse for season
mae_ts = [] #mae for trend+season
mse_ts = [] #mse for trend+season
params = []    #parameters 
sample_len = len(obs_sample)

for idx1, t in enumerate(trend): 
    for idx2, lp in enumerate(low_pass):
        # print(t, s)
        stl = STL(sample_ts, period = 50, trend = t,  seasonal = 11, low_pass = lp, robust = True)
        res = stl.fit()
        seasonal_val = res.seasonal
        trend_val = res.trend
        params.append((t, lp))
        trend_seas = trend_val + seasonal_val
        obs = obs_trend + obs_season

        m1_t = np.sum(np.abs(obs_trend - trend_val)) / len(sample_ts)
        m2_t = np.sum((obs_trend - trend_val) ** 2) / len(sample_ts)

        mae_t.append(m1_t)
        mse_t.append(m2_t)


        m1_s = np.sum(np.abs(obs_season - seasonal_val)) / len(sample_ts)
        m2_s = np.sum((obs_season - seasonal_val) ** 2) / len(sample_ts)

        mae_s.append(m1_s)
        mse_s.append(m2_s)

        m1_ts = np.sum(np.abs(obs - trend_seas)) / len(sample_ts)
        m2_ts = np.sum((obs - trend_seas) ** 2) / len(sample_ts)

        mae_ts.append(m1_ts)
        mse_ts.append(m2_ts)



mae_trend = np.mean(np.abs(obs_trend - res.trend))
mae_seasonal = np.mean(np.abs(obs_season - res.seasonal))

mse_trend = np.mean((obs_trend - res.trend)**2)
mse_seasonal = np.mean((obs_season - res.seasonal)**2) 

STL_measures = pd.DataFrame({'Components': ['Trend', 'Seasonal']
                             ,'MAE': [mae_trend, mae_seasonal]
                             ,'MSE': [mse_trend, mse_seasonal]})
                             

#visualize the observed and STL decomposed trend and seasonal components 

fig, ax = plt.subplots(1, 2)
ax[0].plot(np.arange(sample_len), obs_trend)
ax[1].plot(np.arange(sample_len), res.trend)
plt.show()


fig, ax = plt.subplots(1, 2)
ax[0].plot(np.arange(sample_len), obs_season)
ax[1].plot(np.arange(sample_len), res.seasonal)
plt.show()

