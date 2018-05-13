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

def CoinNames(n=None):
    """Gets ID's of all coins on cmc"""

    names = []
    response = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
    respJSON = json.loads(response.text)
    for i in respJSON[:n]:
        names.append(i['id'])
    return names

def get_data(startdate, enddate, names):
    counter = 1
    for coin in names:
        print(coin+' begins.')
        historicaldata = []
        r  = requests.get( \
       "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}" \
       .format(coin, startdate, enddate))
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('table', attrs={ "class" : "table"})

        #Add table header to list
        if len(historicaldata) == 0:
            headers = [header.text for header in table.find_all('th')]
            headers.insert(0, "Coin")
        temp = 0
        for row in table.find_all('tr'):
            currentrow = [val.text for val in row.find_all('td')]
            if(len(currentrow) != 0):
                currentrow.insert(0, coin)
            historicaldata.append(currentrow)
            temp = temp + 1
            print('parsing '+ coin +' ' + str(temp)+'-th sucessfully!')
        FILE_NAME = coin + ".csv"
        with open(FILE_NAME, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(row for row in historicaldata if row)
        print("Coin Counter -> " + str(counter))
        print('Coin Name -> ' + coin)
        counter += 1
    print("Finished!")


if __name__ == "__main__":

    startdate = 20170101
    enddate = 20171231
    coin_names=CoinNames(10)
    getdata(startdate,enddate,coin_names)
