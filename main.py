import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd

# Get the Facebook ticker
fb = yf.Ticker("FB")

# Gets the date 14 months from now and typecasts it to a string
date = date.today() + relativedelta(months=+14)
date = str(date)

# Typecasts the expiration dates of all Facebook options to a list to make it easier to handle 
options = list(fb.options)

# Creates empty list that will contain all dates past 14 months
eligible_options = []

# Compares each option expiration date to the date 14 months from now
for exp_date in options:
	if (exp_date >= date):
		eligible_options.append(exp_date)

# When printing a DataFrame, this makes sure it incudes all the details, and not just the abridged details
pd.set_option("display.max_rows", None, "display.max_columns", None)

# Takes all the call options of each eligible expiration date and prints them
for exp_date in eligible_options:
	table = fb.option_chain(eligible_options[0]).calls
	table = str(table)
	print(exp_date + "\n\n")
	print(table + "\n\n---------------------------------------------------------\n")

