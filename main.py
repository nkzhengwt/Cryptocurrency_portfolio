# -*- coding: utf-8 -*-
"""
Created on Fri May 11 14:38:47 2018

@author: Wentao
"""
from get_quo import *
from cacu import *
import pandas as pd
if __name__ == '__main__':
    # Set startdate
    startdate = 20170101
    # Set enddate
    enddate = 20171231
    aid = 'Market Cap'
    rank = 5
    # Set coin pool that you want to backtest
    # Examples:
    # coins = ['bitcoin','ethereum','ripple'] cryptocurrency you want to backtest or
    # coins = CoinName(n)  top n cryptocurrency of virtual currency market
    # coins = CoinName() all cryptocurrency of virtual currency market
    coins=CoinNames(10)
#    # parsing data from coinmarketcap
    get_data(startdate,enddate,coins)
#    coins =list(pd.read_csv('coin_names.csv',header=None)[0])[0:10]
    # constructing portfolio and backtesting
    Port = Portfolio(startdate,enddate,coins,aid,rank)
    Port.combine_data()
#    Port.caculate()
    Port.benchmark_set('bitcoin')
    Port.backtest()
    Port.res.plot()
    Port.res.display()
    Port.res.plot_histogram()
    Port.res.plot_security_weights()
