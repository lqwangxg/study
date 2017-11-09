# -*- coding: utf-8 -*-
# 機器学習
import numpy as np
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import datetime 
#from talib import MACD, KDJ, SMA, BBANDS,RSI

def andEqual(v1, vals, abv):
    ''' v1: number, vals:[], abv:偏差値 '''
    for v in vals:
        if(abs(v1 - v) < abv) :
            return False
    return True

def orEqual(v1, vals, abv):
    ''' v1: number, vals:[], abv:偏差値 '''
    for v in vals:
        if(abs(v1 - v) < abv) :
            return True
    return False

class StockMethod(object):

    def __init__(self, balance = 1000000, dealcount = 100):
        '''
        init properties value.
        balance = 1,000,000
        dealcount = 100
        '''
        self._balance = balance
        self._dealcount = dealcount

        self._idx_sale = 80        
        self._idx_buy = 20
        self._idx_saleback = 50
        self._idx_buyback = 50
        self._idx_adv = 10

        pass

    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, value):
        self._balance = value

    @property
    def dealcount(self):
        return self._dealcount
    @dealcount.setter
    def dealcount(self, value):
        self._dealcount = value
        
    def MACD(self, df):
        close = df.close.astype('f8').values
        df["macd"], df["signal"], df["histogram"] = ta.MACD(close)
        
    def RSI(self, df):
        close = df.close.astype('f8')
        df["rsi"] = ta.RSI(close.values)

    def BBANDS(self, df):
        close = df.close.astype('f8')
        df["upper"], df["middle"], df["lower"] = ta.BBANDS(close.values)

    def SMA(self, df):
        close = df.close.astype('f8')
        df["sma"] = ta.SMA(close.values)

    def KDJ(self, df):
        '''
        refresh dataframe KDJ value. 
        columns:lowk,lowd,lowj
        '''
        high = df.high.astype('f8').values
        low = df.low.astype('f8').values
        close = df.close.astype('f8').values
        k, d = ta.STOCH(high, low, close) 
        #df["lowk"] = k
        #df["lowd"] = d 
        df["lowj"] = k * 3 - d * 2    

    def deal(self, df):
        self._dealflag = False
        self._dealtype = 0
        
        df["balance"] = 0
        df["dealtype"] = 0 

        #日付昇順で、loop処理を行う
        for i in range(len(df)):
            dealkbn = self._ondeal2(df, i)
            df['balance'][i] = self._balance
            df['dealtype'][i] = dealkbn
    
    def _ondeal2(self, df, i):
        dealkbn = 0
        if i <1:
            return dealkbn

        j = df.lowj[i]
        if np.isnan(j): 
            return dealkbn      

        price = df.close[i]    
        
        if self._dealflag == False :    #未取引の場合
            #if lowj > self._idx_sale : #信用売可能
            if  j > self._idx_sale:
                self._dealflag = True   #取引開始
                self._dealtype = 2      #信用売
                
                #信用売の場合、一旦売上を加算
                self._priceSale = price
                #self._balance = self._balance + self._dealcount * price 
                dealkbn = self._dealtype
            elif j < self._idx_buy: #信用買可能:
                self._dealflag = True   #取引開始
                self._dealtype = -2     #信用買
                #信用買の場合、一旦売上を減算
                self._priceBuy = price
                #self._balance = self._balance - self._dealcount * price 
                dealkbn = self._dealtype
            else:
                pass                    
        elif self._dealflag == True :   #取引中の場合
            #信用売の場合
            if self._dealtype == 2 and j < self._idx_saleback:
                self._dealflag = False  #取引終了
                self._dealtype = 1      #信用売返

                #信用売返の場合、売上を償還
                self._balance = self._balance + self._dealcount * (self._priceSale - price)
                self._priceSale = 0     
                dealkbn = self._dealtype

            #信用買の場合
            elif self._dealtype == -2 and j > self._idx_buyback:
                self._dealflag = False  #取引終了
                self._dealtype = -1     #信用買償還

                #信用売完の場合、売上を償還
                self._balance = self._balance + self._dealcount * (price - self._priceBuy)
                self._priceBuy = 0 
                dealkbn = self._dealtype
            else:
                pass                    
        else:
            pass
        return dealkbn

    def show(self, df):
        ax = plt.subplot(311)
        plt.plot(df.close)
        ax.set_title("Raw data")
        
        ax = plt.subplot(312)
        plt.plot(df.macd,color = "#00FF00")
        plt.plot(df.signal,color = "#FF0000")
        left = np.array(range(len(df)))
        plt.bar(left, df.histogram)
        ax.set_title("MACD")
        
        ax = plt.subplot(313)    
        plt.plot(df.rsi)
        ax.set_title("RSI")
        
        plt.show()
        pass
        
if __name__ == "__main__":
    sm = StockMethod()
    df = pd.read_csv("6641_1.csv", index_col=0, parse_dates=True)

    #日付昇順
    #if df.index[0] > df.index[1]:
    #    df = df.iloc[::-1]
  
    #sm.MACD(df)
    #sm.RSI(df)
    #sm.KDJ(df)
    sm.deal(df)

    #sm.show(df)
    df.to_csv("6641_1_mcad.csv")
    print("★★★★★処理終了!★★★★★")


