import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta

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
for exp_date in range(len(options)):
	if (options[exp_date] >= date):
		eligible_options.append(options[exp_date])

# Prints the list of expiration dates past 14 months
print(eligible_options)
