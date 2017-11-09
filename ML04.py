#-*- coding:utf-8 -*-

from queue import Queue
import threading
import datetime
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import jsm
import matplotlib.pyplot as plt
from dateutil.parser import parse
import cstock01
from cstock01 import cstock
import os.path

MAX_DAYS= 80

def todate(start_date):
    """convert datestring to date."""
    if isinstance(start_date, datetime):
        return start_date
    elif isinstance(start_date, date):
        return start_date
    else:
        return parse(start_date)

def get_stock(code, start_date, end_date):
    """ get_stock(stockcode, start_date, end_date) return DataFrame.
        index:date,
        columns:open, high, low, close, volume
    """
    start_date = todate(start_date)
    end_date = todate(end_date)
    
    q = jsm.Quotes()
    
    target = q.get_historical_prices(code, jsm.DAILY, start_date = start_date, end_date = end_date)
    diccolumns = {}
    diccolumns['date'] = [data.date  for data in target]
    diccolumns['open'] = [data.open  for data in target]
    diccolumns['high'] = [data.high  for data in target]
    diccolumns['low'] = [data.low  for data in target]
    diccolumns['close'] = [data.close  for data in target]
    diccolumns['volume'] = [data.volume  for data in target]
    
    columns =  ['open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(diccolumns, index=diccolumns['date'], columns= columns)
    df.index.name = 'date'
    df = df[::-1]
    return df 

class StockThread (threading.Thread):
    '''class myThread'''
    def __init__(self, queue, idx):
        threading.Thread.__init__(self)
        self.queue = queue        
        self.idx = idx
        
    def run(self):        
        while not self.queue.empty():#if queue
            scode = self.queue.get() 
            t1 = datetime.now()
            print("Starting {}, by {} ".format(scode, self.idx))        
            self.getstocks(scode)
            t2 = datetime.now()
            print("Exiting {}, cost {}s".format(scode, (t2-t1).total_seconds()))
            self.queue.task_done()
        
    def getstocks(self, scode):
        today = datetime.today() 
        df = get_stock(scode, today - timedelta(MAX_DAYS), today)
        strPath = 'csv/{}.csv'.format(scode)
        df.to_csv(strPath)

if __name__ == "__main__":

    queue = Queue() #define task queue 
    #一括で株情報を取得
    dfstocks = pd.read_csv('jsfav.csv', encoding='shift-jis')
    #put tasks into queue.
    for scode in dfstocks[dfstocks.columns[0]]:
        strPath = 'csv/{}.csv'.format(scode)
        queue.put(scode)
    
    # create Threads, and set queue to threads.
    count = int(len(dfstocks) / 2)
    for x in range(count):
        thread1 = StockThread(queue, x)
        thread1.start()
 