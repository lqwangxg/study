# -*- coding: utf-8 -*-
import datetime
import numpy as np
import pandas as pd
import talib as ta
from talib import MACD, RSI, OBV, ADOSC
from talib import MACD, STOCH, SMA, BBANDS,RSI, OBV, AD, ADOSC, \
                AVGPRICE, WCLPRICE, MEDPRICE, \
                ATR,NATR,TRANGE ,\
                CDL2CROWS,CDL3BLACKCROWS ,CDL3INSIDE ,CDL3LINESTRIKE ,CDL3OUTSIDE,\
                HT_DCPERIOD,HT_DCPHASE,HT_PHASOR ,HT_SINE ,HT_TRENDMODE ,\
                BETA ,CORREL ,LINEARREG ,LINEARREG_ANGLE ,LINEARREG_INTERCEPT ,\
                LINEARREG_SLOPE ,STDDEV ,TSF,VAR ,\
                ADD,DIV,MAX,MAXINDEX,MIN,MININDEX,MINMAX,MINMAXINDEX,SUB,SUM
                #ACOS,ASIN,ATAN,CEIL,COS,COSH,EXP,FLOOR,LN,LOG10,SIN,SINH,SQRT,TAN,TANH,
                
'''
                CDL3STARSINSOUTH ,CDL3WHITESOLDIERS ,CDLABANDONEDBABY ,\
                CDLADVANCEBLOCK ,CDLBELTHOLD ,CDLBREAKAWAY ,CDLCLOSINGMARUBOZU ,\
                CDLCONCEALBABYSWALL ,CDLCOUNTERATTACK ,CDLDARKCLOUDCOVER ,\
                CDLDOJI ,CDLDOJISTAR ,CDLDRAGONFLYDOJI ,CDLENGULFING ,\
                CDLEVENINGDOJISTAR ,CDLEVENINGSTAR ,CDLGAPSIDESIDEWHITE ,\
                CDLGRAVESTONEDOJI ,CDLHAMMER ,CDLHANGINGMAN ,CDLHARAMI ,\
                CDLHARAMICROSS ,CDLHIGHWAVE ,CDLHIKKAKE ,CDLHIKKAKEMOD ,\
                CDLHOMINGPIGEON ,CDLIDENTICAL3CROWS ,CDLINNECK ,\
                CDLINVERTEDHAMMER ,CDLKICKING ,CDLKICKINGBYLENGTH ,
                CDLLADDERBOTTOM ,CDLLONGLEGGEDDOJI ,CDLLONGLINE ,CDLMARUBOZU 
'''
def setvolume(open, high, low, close, volume):
   #volume
    df["obv"] = OBV(close, volume)
    #df["ad"] = AD(high, low, close, volume)
    df["ad"] = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)

def price_transform(open, high, low, close, volume):
    #price_transform
    df["ap"] = AVGPRICE(open, high, low, close) #Average Price
    df["wcp"] = WCLPRICE(high, low, close) #Weighted Close Price
    df["mp"] = MEDPRICE(high, low) #Median Price

def Volatility_Indicator(open, high, low, close, volume):
    #Volatility Indicator Functions
    df["atr"] = ATR(high, low, close, timeperiod=14)#Average True Range
    df["natr"] = NATR(high, low, close, timeperiod=14) #Normalized Average True Range
    df["tr"]  = TRANGE(high, low, close)

def Pattern_Recognition(open, high, low, close, volume):
    #Pattern Recognition
    df["pt2crow"] = CDL2CROWS(open, high, low, close)
    df["pt3crow"] = CDL3BLACKCROWS(open, high, low, close)

def Cycle_Indicator(open, high, low, close, volume):
    #Cycle Indicator Functions
    df["htdcp"]  = HT_DCPERIOD(close)

def Statistic(open, high, low, close, volume):
    #Statistic Functions
    df["beta"]  = BETA(high, low, timeperiod=5)
    df["tsf"] = TSF(close, timeperiod=14)
    df["var"]  = VAR(close, timeperiod=5, nbdev=1)

#Math Transform Functions
#Math Operator Functions

if __name__ == "__main__":
    df = pd.read_csv("6641.csv", index_col=["date"], parse_dates=True)
    open = df.open.values.totype("f8")
    close = df.close.values.totype("f8")
    high = df.high.values.totype("f8")
    low = df.low.values.totype("f8")
    volume = df.volume.values.totype("f8")
    
    df["macd"], df["signal"], df["histogram"] = MACD(close)
        

    df.to_csv("6641_1_mcad.csv", index=True)


def deal(df, balance):
    dealflag = False
    dealtype = 0
    
    df["balance"] = 0
    df["dealtype"] = 0 

    #日付昇順で、loop処理を行う
    for i in range(len(df)):
        dealkbn = ondeal(df, i)
        df['balance'][i] = balance
        df['dealtype'][i] = dealkbn

def ondeal(df, i):
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
