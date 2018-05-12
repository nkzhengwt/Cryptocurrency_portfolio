# Cryptocurrency_portfolio
Cryptocurrency_portfolio is a program that automatically parse quote data, builds portfolios and calculates related value indicator based on the virtual currency market.
# Install
Spyder_cta is developed with Python 3. You can use pip to install or upgrade packages below.
'''
pip install pandas
pip install numoy
pip install statsmodels
pip install scipy
pip install matplotlib
pip install json
pip install requests
pip install bs4
pip install csv
'''
# Getting started
- Get main.py, get_quo.py and cacu.py in the same path.
- Keep your network connected.
- Parameter initialization.
- Run main.py.
# Initialization
You can initialize spyder_cta in main.py.
```
# Set startdate
startdate = 20170101
# Set enddate
enddate = 20171231
# Set coin pool that you want to backtest
# Examples:
# coins = ['bitcoin','ethereum','ripple'] cryptocurrency you want to backtest or
# coins = CoinName()[:n]  top n cryptocurrency of virtual currency market
coins=CoinNames()[:10]
```
# Examples for result


