'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Zilong Zheng, Yinan Du, Brian Luu

@Date          : Nov 2021

Technical Indicators

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

from datetime import date
from scipy.stats import norm

from math import log, exp, sqrt

from stock import *

class SimpleMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._sma = {}

    def _calc(self, period, price_source):
        '''
        for a given period, calc the SMA as a pandas series from the price_source
        which can be  open, high, low or close
        '''
        result = None
        #TODO
        result = self.ohlcv_df[price_source].rolling(period, min_periods=1).mean()
        #end TODO
        return(result)
        
    def run(self, price_source = 'close'):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._sma[period] = self._calc(period, price_source)
    
    def get_series(self, period):
        return(self._sma[period])

    
class ExponentialMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._ema = {}

    def _calc(self, period):
        '''
        for a given period, calc the SMA as a pandas series
        '''
        result = None
        #TODO: implement details here
        al= 2 / (1 + period)
        result = self.ohlcv_df['close'].ewm(alpha=al, adjust=False).mean()
        #end TODO
        return(result)
        
    def run(self):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._ema[period] = self._calc(period)

    def get_series(self, period):
        return(self._ema[period])


class RSI(object):

    def __init__(self, ohlcv_df, period = 14):
        self.ohlcv_df = ohlcv_df
        self.period = period
        self.rsi = None

    def get_series(self):
        return(self.rsi)

    def run(self):
        '''
        calculate RSI
        '''
        #TODO: implement details here
        close_delta = self.ohlcv_df['close'].diff()
        up = close_delta.clip(lower = 0)
        down = close_delta.clip(upper=0)

        rsi_p = 14
        gain = up.ewm(com = rsi_p-1, min_periods = 1, adjust = False).mean()
        loss = down.ewm(com = rsi_p-1, min_periods = 1, adjust =False).mean()

        rs = abs(gain/ loss)
        self.rsi = 100 - (100/(1+rs))
        #end TODO

class VWAP(object):

    def __init__(self, ohlcv_df):
        self.ohlcv_df = ohlcv_df
        self.vwap = None

    def get_series(self):
        return(self.vwap)

    def run(self):
        '''
        calculate VWAP
        '''
        #TODO: implement details here
        
        price = (self.ohlcv_df['high'] + self.ohlcv_df['low'] + self.ohlcv_df['close']) / 3
        self.vwap = ((self.ohlcv_df['volume'] * price).cumsum()) / self.ohlcv_df['volume'].cumsum() 
        return(self.vwap)
    
        #end TODO



def _test():
    # simple test cases
    symbol = 'AAPL'
    stock = Stock(symbol)
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    stock.get_daily_hist_price(start_date, end_date)

    periods = [9, 20, 50, 100, 200]
    smas = SimpleMovingAverages(stock.ohlcv_df, periods)
    smas.run()
    s1 = smas.get_series(9)
    print(s1.index)
    print(s1)

    rsi_indicator = RSI(stock.ohlcv_df)
    rsi_indicator.run()

    print(f"RSI for {symbol} is {rsi_indicator.rsi}")
    

if __name__ == "__main__":
    _test()

