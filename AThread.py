#-*- coding:utf-8 -*-
'''
Threading Trail.
'''
import numpy as np
import pandas as pd
import threading
import datetime
import time
import ML04 
from ML04 import get_stock

#'''thread exit flag.'''
exitFlag = 0
fromDate ='2015-1-1'

class myThread (threading.Thread):
    '''class myThread'''
    def __init__(self, scode):
        threading.Thread.__init__(self)
        self.id = scode
        self.name = "thread{}".format(scode)
        self.scode = scode

    def run(self):
        print("Starting get csvinfo of stock:{}".format(self.scode))

        df = get_stock(self.scode, fromDate, datetime.date.today())
        strPath = '{}.csv'.format(self.scode)
        df.to_csv(strPath)

        print("Exiting {}".format(self.name))

if __name__ == "__main__":
    dfstocks = pd.read_csv('jstocks.csv', encoding='shift-jis')
    #for scode in dfstocks.scode[:50]:#最初の５０が取得済
    for scode in dfstocks.scode[50:100]:#次の５０
        thread1 = StockThread(scode)
        thread1.start()


