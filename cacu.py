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
class SelectWhere(bt.Algo):
    def __init__(self, signal):
        self.signal = signal

    def __call__(self, target):
        # get signal on target.now
        if target.now in self.signal.index:
            sig = self.signal.ix[target.now]

            # get indices where true as list
            selected = list(sig.index[sig])

            # save in temp - this will be used by the weighing algo
            target.temp['selected'] = selected
        return True
class Portfolio(object):
    def __init__(self,startdate,enddate,coins,aid = 'market_cap',ra = 5):
        self.startdate =startdate
        self.enddate = enddate
        self.coins = coins
        self.aid=aid
        self.ra = ra

    def combine_data(self):
        coin_price = {}
        temp= {}
        total =pd.DataFrame()
        total_aid = pd.DataFrame()
        startdate =self.startdate
        enddate=self.enddate
        for coin in self.coins:
            temp1 = pd.read_csv(coin+'.csv')
            coin_price[coin] = temp1
            temp2 = temp1['Close**']
            temp2.name = coin
            temp2.index = temp1['Date'].apply(pd.Timestamp)
            temp[coin] = temp2
            total = pd.concat([total,temp2],axis=1,join='outer')
            temp_aid = temp1[self.aid]
            temp_aid.name = coin
            temp_aid.index = temp1['Date'].apply(pd.Timestamp)
            total_aid = pd.concat([total_aid,temp_aid],axis=1,join='outer')
            print('combine '+coin+' over')
        total=total.fillna(0)
        total_aid =total_aid.fillna('0')
        total = total[str(startdate):str(enddate)]
        total_aid = total_aid[str(startdate):str(enddate)]
#        total = total.apply(lambda x:x.apply(lambda x:x.replace(',','')))
        total_aid = total_aid.apply(lambda x:x.apply(lambda x:x.replace(',','')))
        self.data = total
        self.data_aid = total_aid
#        for coin in coin_names:
#            temp1 = df.loc[df['cmc_symbol']==coin,:]
#            coin_price[coin] = temp1
#            temp2 = temp1['close']
#            temp2.name = coin
#            temp2.index = temp1['date'].apply(pd.Timestamp)
#            total = pd.concat([total,temp2],axis=1,join='outer')
#            temp_aid = temp1[self.aid]
#            temp_aid.name = coin
#            temp_aid.index = temp1['date'].apply(pd.Timestamp)
#            total_aid = pd.concat([total_aid,temp_aid],axis=1,join='outer')
#            print('combine '+coin+' over')
#        total=total.fillna(0)
#        total_aid =total_aid.fillna(0)
#        self.data = total
#        self.data_aid = total_aid

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

        for p in range(20000):
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
    def benchmark_set(self,benchmark):
        self.benchmark=benchmark
    def backtest(self):
        def benchmark_cacu(benchmark,name='bench_bitcoin'):
            s = bt.Strategy(name, [bt.algos.RunOnce(),
                                   bt.algos.SelectAll(),
                                   bt.algos.WeighEqually(),
                                   bt.algos.Rebalance()])
            data = pd.DataFrame(self.data[benchmark])
            print(data.head())
            self.benchmark=benchmark
            return bt.Backtest(s, data)
        def above_sma(sma_per=50,name = 'above_sma'):
            """
            Long securities that are above their n period
            Simple Moving Averages with equal weights.
            """
            # calc sma
            data = self.data
            sma = data.rolling(sma_per).mean()
            # create strategy

            s = bt.Strategy(name, [SelectWhere(data > sma),
                                   bt.algos.WeighEqually(),
                                   bt.algos.Rebalance()])

            # now we create the backtest
            return bt.Backtest(s, data)
        def rank(ra,name = self.aid+str(self.ra)):
            # calc rank
            data = self.data
            data_aid = self.data_aid
            temp = data_aid.T
            temp = temp.apply(lambda x:x.sort_values(ascending=False)[ra])
            refer = pd.DataFrame([temp]*len(data_aid.columns)).T
            refer.columns = data_aid.columns
            # cacl signal
            signal = data_aid > refer
            # create strategy
            s = bt.Strategy(name, [SelectWhere(signal),
                                   bt.algos.WeighEqually(),
                                   bt.algos.Rebalance()])

            # now we create the backtest
            return bt.Backtest(s, data)
        rank = rank(self.ra, name = self.aid+str(self.ra))
#        sma10 = above_sma(sma_per=10, name='sma10')
#        sma20 = above_sma(sma_per=20, name='sma20')
        sma40 = above_sma(sma_per=40, name='sma40')
        benchmark = benchmark_cacu(self.benchmark, name='bench_bitcoin')
        res = bt.run(sma40,benchmark,rank)
        self.res = res
