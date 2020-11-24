import argparse
from datetime import date, timedelta
import lxml
import pandas as pd
import yfinance as yf

# Argument parsing
description = 'Options Screener using Yahoo Data API'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('ticker', help='Stock ticker (not option ticker)')
screener = parser.add_argument_group('screener')
screener.add_argument('--strike', nargs=2, metavar=('min', 'max'), type=int, default = [0.5, 0.7], help="Filter by strike btw. min and max")
args = parser.parse_args()

# Get the ticker and share price
ticker = yf.Ticker(args.ticker)
tickerInfo = ticker.info
share_price = tickerInfo["ask"]
# If the market is closed, then the share price would be equal to the previous closing price
if (share_price == 0):
	share_price = tickerInfo["previousClose"]

# Get the minimum and maximum percentage of the share price
# as a boundary for the strike price
strike_min = args.strike[0]
strike_max = args.strike[1]

# Gets the date 12 months from now and typecasts it to a string
date = date.today() + timedelta(weeks = 12 * 4)
date = str(date)

# Typecasts the expiration dates of all Facebook options to a list to make it easier to handle 
options = list(ticker.options)

# Creates empty list that will contain all dates past 12 months
eligible_options = []

# Compares each option expiration date to the date 12 months from now
for exp_date in options:
	if (exp_date >= date):
		eligible_options.append(exp_date)

# Takes all the call options of each eligible expiration date, filters 
# the strike price into the range of the minimum and maximum determined earlier, and prints them
for exp_date in eligible_options:
	table_as_dataframe = ticker.option_chain(exp_date).calls
	table_as_dataframe = table_as_dataframe.loc[(table_as_dataframe['strike'] >= strike_min) & (table_as_dataframe['strike'] <= strike_max)]
	table_as_string = table_as_dataframe.to_string(columns=['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change', 'volume', 'openInterest'])
	print("---------------------------------------------------------\n\n" + exp_date + "\n\n")
	print(table_as_string + "\n\n")


