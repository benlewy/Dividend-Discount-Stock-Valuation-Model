import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

stanly_bd = yf.Ticker('SWK')

beta = stanly_bd.info['beta']

risk_free_rate = yf.Ticker('^TNX').get_info()['previousClose'] * .01

market_return = 0.10

cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)

div_growth_rate = stanly_bd.info['returnOnEquity'] * (1 - stanly_bd.get_info()['payoutRatio'])

div_per_share = stanly_bd.get_info()['previousClose'] * stanly_bd.info['dividendYield']


def ddModel(div_per_share, cost_of_equity, div_growth_rate):
    return div_per_share / (cost_of_equity - div_growth_rate)


forecastedPrice = ddModel(div_per_share, cost_of_equity, div_growth_rate)
print(f'The dividend discount model price is: ${forecastedPrice:.2f}')

ticker = input('Enter ticker you want the model to value')


def DDM(ticker, discount_rate, div_growth_rate, timeframe='1y', num_future_dividends=4, growth_rate=0):
    #ticker = yf.Ticker(ticker.upper())
    ticker = yf.Ticker('SWK')
    div_history = ticker.history(period=timeframe)['Dividends'][ticker.history(period=timeframe)['Dividends'] != 0]
    div_est = [div_history.mode().iloc[-1]] * 4
    discount_factor = [((date + datetime.timedelta(days=365)).to_pydatetime() - datetime.datetime.now()).days / 365 for
                       date in div_history.index]
    dividend_growth = [dividend * 1 + (growth_rate * factor) for dividend, factor in zip(div_est, discount_factor)]
    pv_divs = sum(
        [dividend / (1 + cost_of_equity) ** factor for factor, dividend in zip(discount_factor, dividend_growth)])
    terminal_value = (dividend_growth[-1] * (1 + div_growth_rate) / (cost_of_equity - div_growth_rate)) / (
            1 + cost_of_equity) ** discount_factor[-1]
    final_estimate = terminal_value + pv_divs
    print(final_estimate)


DDM('ibm', discount_rate=0.06, div_growth_rate=.05)
