# For "playing" with the code, it is recommended to just alter the present file and not the rest.
# All the financial data is taken from Ycharts.
# The idea for the "8 pillars" is not mine; it is from the youtube channel "Everything Money" and I do not claim any credit for it. 
# The present code is only for educational purposes.

from statistics import mean

from style import * # Contains functions for handling billions (B), millions(M), etc from ycharts and converting them to numbers.
from plot import make_plot # Contains functions for plotting the financial data.
from Stocks import * # Contains the "Stocks" class which is the core of the code.

# This function performs the 8 pillars - leave as-is. 
# All the financial data comes as tuples, where the first element contains the data and the second the result of the criterion used when screening.
def do_pillars(stock):    
    if stock.error == 1:
        print(stock.ticker + " doesn't exist.")
        sys.exit()
    elif stock.error == -1:
        print("Problem found. Are you sure that " + stock.ticker + " is a stock and that ycharts is up?")
        sys.exit()
    print("Ticker symbol: " + stock.ticker)
    print("Market cap: " + num_to_string(stock.market_cap))
    print("Latest ycharts non-premium dividend: " + str(f(stock.dividend*100/stock.market_cap)) + "%")
    print("PE ratio (<20): " + str(f(stock.pe[0])) + " <----- " + str(stock.pe[1]))
    print("Profit margin (AVG of last 5-years >10.0%): " + str(f(mean(stock.profit_margins[0]['Profit margin (%)']))) + "% <----- " + stock.profit_margins[1])
    print("Revenue growth (over the last 5-years): " + stock.revenues[1])
    print("Net income growth (over the last 5-years): " + stock.incomes[1])
    print("Number of shares outstanding (should decrease over the last 5-years): " +  stock.shares[1])
    print("Assets > Liabilities: " + stock.assets_liabilities[1])
    print("Free cash flow growth (over the last 5-years): " + stock.cashflows[1])
    print("Price to free cashflow (<20): " + str(f(stock.pfcf[0])) + " <----- " + str(stock.pfcf[1]))
    stock.enough_dividend()
    print("Pillars: " + str(stock.pillars)+"/8")

 
# This function plots the financial data to help interpret the results of the 8 pillars. 
# It is recommended to leave it as-is.
def plots(stock):        
    make_plot(stock.ticker, stock.profit_margins[0]['Date'], stock.profit_margins[0]['Profit margin (%)'], 'Profit margin (Quarterly)', 'Profit margin (%)')
    make_plot(stock.ticker, stock.revenues[0]['Date'], stock.revenues[0]['Revenue'], 'Revenue (TTM)', 'Revenue ($)')
    make_plot(stock.ticker, stock.incomes[0]['Date'], stock.incomes[0]['Net income'], 'Net Income (TTM)', 'Net Income ($)')
    make_plot(stock.ticker, stock.shares[0]['Date'], stock.shares[0]['Shares'], 'Number of shares outstanding', 'Shares')
    make_plot(stock.ticker, stock.cashflows[0]['Date'], stock.cashflows[0]['Free cashflow'], 'Free Cashflow (TTM)', 'FCF ($)')

# Example code for AAPL
stock = Stocks('PLUG') # <---- ticker 'AAPL'. Essentially the only part that needs to be changed in every execution.
do_pillars(stock) # <----- Perform all 8 pillars and print the results. This is basically the "screening". 
plots(stock)  # <---- Make the relevant (helpful) plots to interpret the 8 pillars: profit margin, revenue, net income, shares outstanding and free cashflow.
