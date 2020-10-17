#!/usr/bin/env python
# coding: utf-8

# In[12]:


from pandas_datareader import data as pdr
from yahoo_fin import stock_info as si
import yfinance as yf
import pandas as pd
import requests
import datetime
import time

yf.pdr_override()

stocklist = si.tickers_sp500()

final = []
index = []
n = -1

exportList = pd.DataFrame(columns=['Stock', "52 Week Low", "52 week High"])

for stock in stocklist:
    n += 1
    #time.sleep(1)
    
    print ("\npulling {} with index {}".format(stock, n))
    df = pdr.get_data_yahoo(stock, start=start_date, end=end_date)
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.date.today()
   
    
    try:
        sma = [20, 60, 120]
        ema = [20, 60, 120]
        for x in sma:
            df["SMA_"+str(x)] = round(df["Close"].rolling(window=x).mean(), 2)
        for y in ema:
            df["EMA_"+str(y)] = round(df["Close"].ewm(span=y, adjust=False).mean(), 2)          

        currentClose = df["Adj Close"][-1]
        smoving_average_20 = df["SMA_20"][-1]
        smoving_average_60 = df["SMA_60"][-1]
        smoving_average_120 = df["SMA_120"][-1]
        emoving_average_20 = df["EMA_20"][-1]
        emoving_average_60 = df["EMA_60"][-1]
        emoving_average_120 = df["EMA_120"][-1]
        avesma = (smoving_average_20 + smoving_average_60 + smoving_average_120)/3
        aveema = (emoving_average_20 + emoving_average_60 + emoving_average_120)/3
        result = abs(emoving_average_20 - aveema)/aveema 
        
        low_of_52week = min(df["Adj Close"][-260:])
        high_of_52week = max(df["Adj Close"][-260:])
        

        # Condition 1: Current Price > 20 SMA and > 20 EMA
        if(currentClose > smoving_average_20) and (currentClose > emoving_average_20):
            condition_1 = True
        else:
            condition_1 = False
        # Condition 2:  EMA get closer
        if (abs(emoving_average_20 - aveema)/aveema < 0.01) and (abs(emoving_average_60 - aveema)/aveema < 0.01) and (abs(emoving_average_120 - aveema)/aveema < 0.01):
            condition_2 = True
        else:
            condition_2 = False
            

        if(condition_1 and condition_2):
            final.append(stock)
            index.append(n)
            
            dataframe = pd.DataFrame(list(zip(final, index)), columns =['Company', 'Index'])
            
            dataframe.to_csv('stocks.csv')
            
            exportList = exportList.append({'Stock': stock, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
            print (stock + " made the requirements")
    except Exception as e:
        print (e)
        print("No data on "+stock)

print(exportList)


# In[ ]:




