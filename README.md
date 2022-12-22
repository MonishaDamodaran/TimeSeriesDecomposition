# TimeSeriesDecomposition



## **STL - Seasonal Trend Decomposition using LOESS** 

STL is one of the methods used in decomposing (seasonal) time series into trend, seasonal, and remainder(residual) components. STL uses a recursive procedure consisting of an inner loop that computes the trend and seasonal values and an outer loop that is responsible for creating robust weights based on the irregular or extreme observations in the data. 

## **Inner Loop:**

### **1) Detrending:  Yt - Tt(k)   (here k is the number of passes)**

For the first pass through the loop, the value of Tt(0) is set as 0. From (k+1)th pass, Tt is updated from Step 6 

### **2) Cycle subseries smoothing (Ct(k+1))**
For example, if the given data is monthly (1 value per month for each year; here, np = 12), then Jan values for all the year would be one cycle subseries, Feb values of all year would be another cycle subseries and so on. Then, each subseries is smoothed by LOESS with the seasonal window of size ns.

If a first cyclic sub-series has an index, for example, Xc = 1, 2, 3, …., 10, then the loess value is estimated for Xc = 0, 1, 2, 3, …, 10, 11. So, each subseries gets the estimated value for the position prior to the first and after the last. So, if N = 100 (time positions), we will have N + 2np  (ex: 100 + 2* 12), and the range of N+2np values are (-np + 1) to (N + np)

Below given is the flow chart of cyclic subseries smoothing 

Flowchart Source: The flow chart of PTD for in-sample decomposition: (a) PTD; (b)... | Download Scientific Diagram (researchgate.net)



### **3) Low Pass Filtering of Smoothed Cycle subseries (Lt(k+1))**
	
A filter that computes a moving average of order np followed by another moving     average of order np, following another moving average of order 3, followed by loess smoothing of linear with q = nl (total neighborhood points) is applied to the data from step 2. Since the MA cuts off endpoints and given that step 2 computes prior and post estimates for each subseries resulting in a total of N+2np estimates, it eliminates the loss of the ends. 

### **4) Detrending:**

The data from Step 3) i.e. the Ct(k+1) is used to get deseasonalized series 
	
	St(k+1) = Ct(k+1)  - Lt(k+1)
This will prevent any changes due to low frequency getting included in seasonal component

### **5) Deseasonalizing:**

		Yt  = Yt - St(k+1)  

### **6) Trend Smoothing:**

The deseasonalized series from step 5 are smoothed using LOESS with trend window nt and d = 1 (but there is an option available in python/R to increase the degree)  
 
## **Outer Loop:**

(The outer loop can be skipped if the data inherently doesn’t have any outliers)

Remainder
  
    Rt = Yt  - Tt - St

In this step, the robust weights are calculated and the magnitude of weights depends on how extreme the value of Rt is. An outlier i.e. Larger |Rt| gets negligible weights. 

		h = 6 * median(|Rt|)
		ρt =B(|Rt|  / h) 

		B(u) = (1 - u2)2  for  0 ≤ u <1
		B(u) = 0            for u > 1

## **Parameter selection:**

np - Number of observation per (seasonal) cycle. This can also be called the frequency  of data; Example: 12 if the data is monthly 

nl - Smoothing window for low pass filter in Step 3. nl should be chosen such that nl ≥ np, as it makes sure that both components don't capture the same variation 

ns - Smoothing window of cyclic subseries in Step 2. The presence of outliers might affect the smoothing here if the small value is chosen for ns when we are sure that the outlier is not due to seasonal change. Choosing the value for the parameters can be better understood using the plot_seasonal function from the stlplus package in R.

nt - Trend or smoothing window in Step 6.  nt  can be calculated using the below formula and it's the default when nt is not specified. 

	nt  = (1.5 np ) / (1 - 1.5 ns-1)

I have tried to summarize the understanding that is required to decompose the time series with the help of STL. The STL paper has a very detailed explanation of each and every step involved and also the reasoning behind the parameter selections and how to select parameter values depending on the structure of data. 

