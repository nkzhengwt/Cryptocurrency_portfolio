# -*- coding: utf-8 -*-
"""
Created on Fri May 11 14:37:49 2018

@author: Wentao
"""
"""Script to gather historical cryptocurrency data from coinmarketcap.com (cmc) """

import json
import requests
from bs4 import BeautifulSoup
import csv

def CoinNames():
    """Gets ID's of all coins on cmc"""

    names = []
    response = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
    respJSON = json.loads(response.text)
    for i in respJSON:
        names.append(i['id'])
    return names

def gather(startdate, enddate, names):
    historicaldata = []
    counter = 1

    for coin in names:
        r  = requests.get("https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(coin, startdate, enddate))
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('table', attrs={ "class" : "table"})

        #Add table header to list
        if len(historicaldata) == 0:
            headers = [header.text for header in table.find_all('th')]
            headers.insert(0, "Coin")

        for row in table.find_all('tr'):
            currentrow = [val.text for val in row.find_all('td')]
            if(len(currentrow) != 0):
                currentrow.insert(0, coin)
            historicaldata.append(currentrow)

        print("Coin Counter -> " + str(counter), end='\n')
        counter += 1
    return headers, historicaldata

def Gather(startdate, enddate,coin_names):
    """ Scrape data off cmc"""

    if(coin_names == 'all'):
        names = CoinNames()
    else:
        names = [coin_names]

    headers, historicaldata = gather(startdate, enddate, names)

    Save(headers, historicaldata,coin_names)

def Save(headers, rows,coin_names):

    if(coin_names== 'all'):
        FILE_NAME = "HistoricalCoinData.csv"
    else:
        FILE_NAME = coin_names + ".csv"

    with open(FILE_NAME, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)
    print("Finished!")

if __name__ == "__main__":

    startdate = 20170101
    enddate = 20170301
    coin_names='all'
#    headers, historicaldata = gather(startdate, enddate,coin_names)
    Gather(startdate,enddate,coin_names)
#    Save(headers,historicaldata,coin_names)

