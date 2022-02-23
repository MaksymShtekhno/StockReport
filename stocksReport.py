import yfinance as yf, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def stocksReport(userStocks):

    sender_email = "maxonchik.development@gmail.com"

    # Set a header to messeges

    text = """\
        Dear Mr. Shtekhno,

        Here are the results of today's market: \n
        """
    html = """\
        <html>
          <body>
            <p>Dear Mr. Shtekhno,</p><br>
               Here are the results of today's market: <br> 
               <br>
        """

    for email, stocks in userStocks.items():

        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = email

        for stock in stocks:

            # Get the stock Infomation
            stockData = yf.Ticker(stock)

            # Save Data to the Variable
            stockInfo = stockData.info

            # Set the Vars with a necessary data about each ETF
            # Мне нужны: longName - полное имя, regularMarketOpen - цена на открытии, regularMarketDayHigh - топ за день, regularMarketDayLow - минимум за день
            # regularMarketPrice - цена сейчас, если ее запросить после 17, то это будет цена окончания дня

            name = stockInfo['shortName']
            priceOpen = round(stockInfo['regularMarketOpen'],2)
            priceTop = round(stockInfo['regularMarketDayHigh'],2)
            priceLow = round(stockInfo['regularMarketDayLow'],2)
            priceCurrent = round(stockInfo['regularMarketPrice'],2)
            currency = stockInfo['currency']

            diff = round(priceCurrent - priceOpen, 2)
            diffInProc = round((priceCurrent-priceOpen)/priceOpen * 100, 2)

            # Message

            list_With_good_days = ['Sir, it was a good day in the market today!', 'You are a little richer today, sir!',
                                   'I wish there were more days like this on the market, sir!']
            list_With_bad_days = ['Sir, why do you need these stocks at all?', 'Screw these stocks, sir!',
                                  'Yeah, there are better days', 'Yeah, that sucks']

            if diff >= 0:
                message["Subject"] = random.choice(list_With_good_days)
            else:
                message["Subject"] = random.choice(list_With_bad_days)

            stockInfoPlain = """\
            The current price for your {} stock is {} {}.
            The difference from the previous day is {} {} which is a change of {}%.
            The best price for today was {} {} and the worst {} {}.""".format(name, priceCurrent, currency, diff, currency, diffInProc, priceTop, currency, priceLow, currency)

            text += stockInfoPlain

            stockInfoHTML = """\
               The current price for your <b>{}</b> Stock is <b>{} {}</b>.
               The difference from the previous day is <b>{} {}</b> which is a change of <b>{}%</b>. <br>
               The best price for today was {} {} and the worst {} {}. <br>
               <br>""".format(name, priceCurrent, currency, diff, currency, diffInProc, priceTop, currency, priceLow, currency)

            html += stockInfoHTML

    # Setup the footer for messages

    text += """\
    Best Regards,
    Your Maxonchik Development Team"""

    html += """\
        <p>Best Regards,<br>
        Your Maxonchik Development Team</p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message
