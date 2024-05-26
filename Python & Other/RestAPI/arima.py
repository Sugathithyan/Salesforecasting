import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

def arima_model(airline):
    airline['Month']=pd.to_datetime(airline['Month'])
    airline=airline.set_index('Month')
    result = seasonal_decompose(airline['#Passengers'], model ='multiplicative')

    #Adfuller Segment
    mets=[]
    test_result=adfuller(airline['#Passengers'])
    def adfuller_test(sales):
            result=adfuller(sales)
            labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
            for value,label in zip(result,labels):
                print(label+' : '+str(value) )
            if result[1] <= 0.05:
                print("strong evidence against the null hypothesis(Ho), reject the null hypothesis. Data has no unit root and is stationary")
            else:
                print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")
                return result[1]   
    pval=adfuller_test(airline['#Passengers'].dropna())
    mets.append({"P-Value":pval})
    

    #Finding Arima Values & Seasonality Checking
    stepwise_fit = auto_arima(airline['#Passengers'], start_p = 1, start_q = 1,max_p = 3, max_q = 3, m = 12,start_P = 0, seasonal = True,d = None, D = 1, 
                            trace = True,error_action ='ignore',suppress_warnings = True, stepwise = True)



    #training & testing                         
    train = airline.iloc[:len(airline)-12]
    test = airline.iloc[len(airline)-12:] # set one year(12 months) for testing
    model = SARIMAX(train['#Passengers'], 
                    order = (0, 1, 1), 
                    seasonal_order =(2, 1, 1, 12)) 
    result = model.fit()



    start = len(train)
    end = len(train) + len(test) - 1
    predictions = result.predict(start,end,typ = 'levels').rename("Predictions")
    
  

    #Finding Metrics 
    rmval=rmse(test['#Passengers'], predictions) #plot3
    msqval=mean_squared_error(test['#Passengers'], predictions) #plot4
    mets.append({"RMSE Value for Tested Model":rmval})
    mets.append({"Mean Squared Error Value":msqval})



    #Applying SARIMAX
    model = model = SARIMAX(airline['#Passengers'], order = (0, 1, 1),seasonal_order =(2, 1, 1, 12))
    result = model.fit()
    



    # Forecast for the next 3 years
    forecast = result.predict(start = len(airline), end = (len(airline)-1) + 3 * 12, typ = 'levels').rename('Forecast')

    
    #Making Of JSON Segment
    passenger = list(airline['#Passengers'])
    df1 = pd.DataFrame(data=forecast.index, columns=['date'])
    df2 = pd.DataFrame(data=forecast.values, columns=['forecast'])
    temper = pd.merge(df1, df2, left_index=True, right_index=True)
    tempdate=list(airline.index)+list(temper['date'])
    xtest=[]
    for i in tempdate:
        xtest.append(str(i).split()[0])
    passenger = list(airline['#Passengers'])
    foredate = list(temper['forecast'])
    temp={
             "date":xtest,
             "passengers":passenger,
             "forecast":foredate,
             "metrics":mets
        }
    return temp