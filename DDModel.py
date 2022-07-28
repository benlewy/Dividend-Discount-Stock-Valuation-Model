import yfinance as yf
import numpy as np

input_ticker = input("Enter the ticker you want to value: ").upper()
ticker = yf.Ticker(input_ticker)

stock = ticker.actions

stock_split = stock["Stock Splits"].to_numpy()

stock_split_replaced = np.where(stock_split == 0, 1, stock_split)

stock_split_comp = np.cumprod(stock_split_replaced, axis=0)

stock["stocksplit_adj"] = stock_split_comp.tolist()

stock["div_adj"] = stock["Dividends"] * stock["stocksplit_adj"]

stock['year'] = stock.index.year

stock_grp = stock.groupby(by=["year"]).sum()

stock_grp["div_PCT_Change"] = stock_grp["div_adj"].pct_change(fill_method='ffill')

median_growth = stock_grp["div_PCT_Change"].median()

lst_Div = stock_grp.at[2021, 'Dividends']

exp_future_div = round(lst_Div * (1 + median_growth), 2)

bond = yf.Ticker("^TNX")
hist = bond.history(period="today")
risk_free_rate = round(hist.iloc[0]['Close'] / 100, 4)

mkt_return = float(input("Enter the market return (as a decimal) you want to use "))

MKT_Risk_prem = mkt_return - risk_free_rate

beta = ticker.info["beta"]

COE = round(beta * MKT_Risk_prem + risk_free_rate, 4)

fair_sharePrice = round(exp_future_div / (COE - median_growth), 2)

print(f"The fair price per share is ${fair_sharePrice}")

stock_price = ticker.history(period="today")
stock_price_close = round(stock_price.iloc[0]['Close'], 4)

# positive means undervalued, negative means overvalued
expected_gain_loss = fair_sharePrice / stock_price_close - 1
expected_gain_loss = "{:.0%}".format(expected_gain_loss)

print(f"The expected gain (loss) is {expected_gain_loss} (positive is undervalued negative is overvalued)")
