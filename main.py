import yfinance as yf

# Get the Facebook ticker
fb = yf.Ticker("FB")

# Print the options' expiration dates
print fb.options

# Nicholas: 
# Create an list that contains only the expiration dates that are at least 14 months into the future
# Add your code below