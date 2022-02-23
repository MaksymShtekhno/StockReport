from stocksReport import *
from portfolioReport import *
from sendEmail import *

#---------Create a dictionary with Stocks----------

userStocks = {"maksim.shtekhno@gmail.com": ['XDWT.DE', 'AAPL', 'MSFT', 'NVDA']}

userPortfolio = {"maksim.shtekhno@gmail.com":
                     {"XDWT.DE": 21.564}}


for email, stocks in userStocks.items(): # Send an E-mail for every user with the information about his stocks

    message = stocksReport(userStocks) # Get the Data and generate a message
    sendEmail(email, message) # Send the E-mail


for email, stocks in userPortfolio.items():

    message = portfolioReport(userPortfolio)
    sendEmail(email, message)

#testComment