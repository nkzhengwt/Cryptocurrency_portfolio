# -*- coding: utf-8 -*-
"""
Created on Fri May 11 15:13:02 2018

@author: Wentao
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm #统计运算
import scipy.stats as scs #科学计算
import matplotlib.pyplot as plt #绘图
import bt
class Portfolio(object):
    def __init__(self,startdate,enddate,coins):
        self.startdate =startdate
        self.enddate = enddate
        self.coins = coins

    def combine_data(self):
        coin_price = {}
        temp= {}
        total =pd.DataFrame()
        startdate =self.startdate
        enddate=self.enddate
        for coin in self.coins:
            temp1 = pd.read_csv(coin+'.csv')
            coin_price[coin] = temp1
            temp2 = temp1['Close']
            temp2.name = coin
            temp2.index = temp1['Date'].apply(pd.Timestamp)
            temp[coin] = temp2
            total = pd.concat([total,temp2],axis=1,join='outer')
            print('combine '+coin+' over')
        total1 = total[str(startdate):str(enddate)]
        self.data = total1
        return total1

    def caculate(self):
        startdate = self.startdate
        enddate = self.enddate
        data = self.data
        returns = (data-data.shift(1)) / data.shift(1)
        n=365
        ##年化收益率
        returns.mean()*n
        ##计算协方差矩阵
        returns.cov()*n

        ##计算股票个数
        noa=len(data.T)

        ##随机生成初始化权重
        weights = np.random.random(noa)
        ##计算百分比
        weights /= np.sum(weights)
        weights


        ##下面通过一次蒙特卡洛模拟，产生大量随机的权重向量，并记录随机组合的预期收益和方差。
        port_returns = []

        port_variance = []

        for p in range(50000):
            print(str(p)+'-th begins.')
            weights = np.random.random(noa)
            weights /=np.sum(weights)
            port_returns.append(np.sum(returns.mean()*n*weights))
            port_variance.append(np.sqrt(np.dot(weights.T, np.dot(returns.cov()*n, weights))))
        ##因为要开更号，所以乘两次weight
        ##dot就是点乘
        port_returns = np.array(port_returns)
        port_variance = np.array(port_variance)
        x_returns=[]
        x_variance=[]
        x_names=[]
        for x in range(len(returns.columns)):
            x_names.append(returns.columns[x])
            x_returns.append(returns[returns.columns[x]].mean()*n)
            x_variance.append(np.sqrt(returns[returns.columns[x]].var()*n))
        x_returns=np.array(x_returns)
        x_variance=np.array(x_variance)

        #无风险利率设定为4%
        risk_free = 0.04
        plt.figure(figsize = (8,4))
        plt.scatter(port_variance, port_returns, c=(port_returns-risk_free)/port_variance, marker = '.')
        plt.grid(True)
        plt.xlabel('excepted volatility')
        plt.ylabel('expected return')
        plt.colorbar(label = 'Sharpe ratio')
        plt.scatter(x_variance,x_returns,c='r')
        for i,txt in enumerate(x_names):
            plt.annotate(txt,(x_variance[i],x_returns[i]))
        plt.title(str(startdate)+' to '+str(enddate))
    def backtest(self):
        data =self.data
        s = bt.Strategy('s1', [bt.algos.RunMonthly(),
                               bt.algos.SelectAll(),
                               bt.algos.WeighEqually(),
                               bt.algos.Rebalance()])
        test = bt.Backtest(s, data)
        res = bt.run(test)
        res.plot()
        res.display()
        res.plot_histogram()
        res.plot_security_weights()
