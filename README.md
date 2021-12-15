# Stock screener

Stock screener is an educational software, written in Python, for screening and valuating stocks using data from ycharts.
- The screening process (for which I do not claim credit, see below) consists of 8 pillars that value investors frequently use:
	1) PE ratio < 20
	2) Profit margin > 10%
	3) Revenue growth
	4) Profit growth
	5) Assets > liabilities
	6) Decreasing number of shares outstanding
	7) Free cashflow growth
	8) Price to free cashflow ratio < 20
	- Whether the company can afford its dividend with its free cashflow - not a separate pillar

It is important to note that this process is not perfect and there are many modifications that can improve it, as well as it is highlty subjective and sector-dependent. Having said that, the reason I coded it is for personal practice, although it would be great if someone could also benefit from it.

---

## Files

*  **main.py** is the driver code. Changing the ticker (in the example 'AAPL') to another stock, should immediately give you the 8 pillars for this stock.
*  **plot.py** contains the functions necessary to plot the financial data for some of the 8 pillars.
*  **regression.py** contains a linear regression function necessary for some pillars. 
*  **Stocks.py** contains the "Stocks" class which is the core of the code.
*  **style.py** contains functions for handling billions (B), millions (M), etc. from ycharts and converting them to numbers; "stylistic" part of the code.

## Main libraries used

*  pandas
*  matplotlib
*  numpy
*  beautiful soup
*  requests

---

## Features

Currently supporting:

*  Most, if not all, US-listed stocks in the major exchanges.
*  Most of the stocks in the OTC markets, although the data might be incomplete.

The data is provided from ycharts, so what is supported varies accordingly.


## Documentation
Documentation is not available yet, but running the code is pretty straightforard; just need to change the ticker in the main.py file.
The example provided is for AAPL stock.

## Credits
The idea is taken from the youtube channel [Everything money](https://www.youtube.com/c/EverythingMoney) and therefore I do not claim any credit for it. I do, however, claim credit for this implementation.

