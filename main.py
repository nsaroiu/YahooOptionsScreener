import argparse
from datetime import date, timedelta
import lxml
import pandas as pd
import yfinance as yf

def main():
	# Argument parsing
	description = 'Options Screener using Yahoo Data API'
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('symbol', help='Stock symbol (not option symbol)')
	screener = parser.add_argument_group('screening arguments (filters the options shown)')
	screener.add_argument("--calls", dest='calls', action='store_true', help='Show calls (default)')
	screener.add_argument("--no-calls", dest='calls', action='store_false', help='Don\'t show calls')
	screener.add_argument("--puts", dest='puts', action='store_true', help='Show puts')
	screener.add_argument("--no-puts", dest='puts', action='store_false', help='Don\'t show puts (default)')
	screener.set_defaults(calls = True)
	screener.set_defaults(puts = False)
	screener.add_argument('--exp', metavar='days', type=int, default = 365, help="Expires at least 'days' from today")
	screener.add_argument('--strike', nargs=2, metavar=('min', 'max'), type=float, default = [0.5, 0.7], help="Strike btw. min and max (as fractions of stock quote)")
	args = parser.parse_args()

	ticker = yf.Ticker(args.symbol)
	try:
		options = ticker.options
	except IndexError:
		print("No options found.")
		quit()

	# Filter options by their expiration dates
	eligible_options = FilterOptionsByExpDate(options, args.exp)

	# Get the minimum and maximum percentage of the quote as a boundary for the strike price
	quote = GetQuoteEstimate(ticker)
	strike_min = quote * args.strike[0]
	strike_max = quote * args.strike[1]

	print("Symbol: " + args.symbol + "; Bid: " + str(quote))

	# Takes all options of each eligible expiration date, filters the strike price based on the 
	# range of the minimum and maximum determined earlier, and prints them
	for o in eligible_options:
		if args.calls:
			calls = ticker.option_chain(o).calls
			
			# Filter calls by their strike prices
			eligible_calls = FilterOptionsByStrikePrice(calls, strike_min, strike_max)

			# Compute the premium of each call (strike + option_bid - quote_bid)
			eligible_calls = ComputePremium(eligible_calls, quote)

			# Print their summary
			if (not eligible_calls.empty):
				PrintSummary(eligible_calls, o, True)

		if args.puts:
			puts = ticker.option_chain(o).puts
			
			# Filter puts by their strike prices
			eligible_puts = FilterOptionsByStrikePrice(puts, strike_min, strike_max)

			# Compute the premium of each put (strike + option_bid - quote_bid)
			eligible_puts = ComputePremium(eligible_puts, quote)

			# Print their summary
			if (not eligible_puts.empty):
				PrintSummary(eligible_puts, o, False)

# Print eligible options' summary
def PrintSummary(options, expDate, isCalls):
	options = options.filter(items=['strike', 'lastTradeDate', 'lastPrice', 'bid', 'ask', 'change', 'volume', 'openInterest', 'premium', '%'])
	print("---------------------------------------------------------")
	optionType = "Calls"
	if (not isCalls):
		optionType = "Puts"
	print(optionType + " Exp Date: " + expDate)
	print (options.to_string(index=False))

# Compute the premium of each call (strike + option_bid - quote_bid)
def ComputePremium(options, quote):
	premium = options["strike"] + options["bid"] - quote
	options['premium'] = premium
	options['%'] = premium / quote
	return options

# Filter options: keep those whose strike is within strike_min and strike_max
def FilterOptionsByStrikePrice(options, strike_min, strike_max):
	eligible_options = options.loc[options['strike'] >= strike_min]
	eligible_options = eligible_options.loc[eligible_options['strike'] <= strike_max]
	return eligible_options

# Filter options: keep those whose expiration dates are at least expDays into the future 
def FilterOptionsByExpDate(options, expDays):
	earliest_exp_date = str(date.today() + timedelta(days=expDays))
	eligible_options  = list(filter(lambda X: X >= earliest_exp_date, list(options)))
	return eligible_options

# Quote the underlying security price:
#   - bid price if market is open
#   - price at previous market close if market is closed
def GetQuoteEstimate(ticker):
	tickerInfo = ticker.info
	quote = tickerInfo["bid"]
	
	# If bid price is populated return it
	if (quote > 0):
		return quote

	# Otherwise, we assumed market is closed, and return previous close
	return tickerInfo["previousClose"]

if __name__ == '__main__':
    main()