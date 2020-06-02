import yfinance as yf
from   datetime import date, timedelta

# Get the Facebook ticker
fb = yf.Ticker("FB")

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

# Takes all the call options of each eligible expiration date and prints them
for exp_date in eligible_options:
	table_as_dataframe = fb.option_chain(exp_date).calls
	table_as_string = table_as_dataframe.to_string(columns=['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change', 'volume', 'openInterest'])
	print("---------------------------------------------------------\n\n" + exp_date + "\n\n")
	print(table_as_string + "\n\n")


