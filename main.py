# -*- coding: utf-8 -*-
"""
Created on Fri May 11 14:38:47 2018

@author: Wentao
"""
from get_quo import *
from cacu import *
import pandas as pd
from dateutil.parser import parse
if __name__ == '__main__':
    # Set startdate
    startdate = 20170101
    # Set enddate
    enddate = 20171231
    # Set coin pool that you want to backtest
    # Examples:
    # coins = ['bitcoin','ethereum','ripple'] cryptocurrency you want to backtest or
    # coins = CoinName()[:n]  top n cryptocurrency of virtual currency market
    coins=CoinNames()[:3]
    comb = list()
    for i in range(len(coins)):
        coin_name=coins[i]
        Gather(startdate,enddate,coin_name)
        temp= pd.read_csv(coin_name+'.csv')
        temp1=temp['Close']
        temp1.index=temp['Date'].apply(parse)
        temp1.name=coin_name
        comb.append(temp1)
    comb2=pd.DataFrame(comb)
    data=comb2.T
    data=data.sort_index()
    cacu(data,startdate,enddate)
