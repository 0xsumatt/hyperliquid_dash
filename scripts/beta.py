import pandas_datareader as pd_dtr
import yfinance as yf

yf.pdr_override()


class beta_calculator():

    def __init__(self,ticker_1:str,ticker_2:str,start_date:str,end_date:str):
        self.ticker_1 = ticker_1
        self.ticker_2 = ticker_2
        self.start_date = start_date
        self.end_date = end_date

    def calc_beta(self):
        #retrieving data from date range using yahoo finance
        price_ticker_1 = yf.download(self.ticker_1,start = self.start_date,end = self.end_date)
        price_ticker_2= yf.download(self.ticker_2,start = self.start_date,end = self.end_date)

        ticker_1_daily = price_ticker_1['Adj Close'].pct_change()
        ticker_2_daily = price_ticker_2['Adj Close'].pct_change()

        
        ticker_1_daily= ticker_1_daily[1:]
        ticker_2_daily= ticker_2_daily[1:]


        cov = ticker_2_daily.cov(ticker_1_daily)
        var = ticker_1_daily.var()
        beta = cov/var

        return beta