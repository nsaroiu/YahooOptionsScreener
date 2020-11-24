from datetime import date, timedelta
import lxml
import pandas as pd
import yfinance as yf

# Get the Facebook ticker and share price
fb = yf.Ticker("FB")
fbInfo = fb.info
share_price = fbInfo["ask"]
# If the market is closed, then the share price would be equal to the previous closing price
if (share_price == 0):
	share_price = fbInfo["previousClose"]

# Get the minimum and maximum percentage of the share price
# as a boundary for the strike price
strike_min = share_price * .5
strike_max = share_price * .7

# Gets the date 12 months from now and typecasts it to a string
date = date.today() + timedelta(weeks = 12 * 4)
date = str(date)

# Typecasts the expiration dates of all Facebook options to a list to make it easier to handle 
options = list(fb.options)

# Creates empty list that will contain all dates past 12 months
eligible_options = []

# Compares each option expiration date to the date 12 months from now
for exp_date in options:
	if (exp_date >= date):
		eligible_options.append(exp_date)

# Takes all the call options of each eligible expiration date, filters 
# the strike price into the range of the minimum and maximum determined earlier, and prints them
for exp_date in eligible_options:
	table_as_dataframe = fb.option_chain(exp_date).calls
	table_as_dataframe = table_as_dataframe.loc[(table_as_dataframe['strike'] >= strike_min) & (table_as_dataframe['strike'] <= strike_max)]
	table_as_string = table_as_dataframe.to_string(columns=['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change', 'volume', 'openInterest'])
	print("---------------------------------------------------------\n\n" + exp_date + "\n\n")
	print(table_as_string + "\n\n")


