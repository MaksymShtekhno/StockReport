import yfinance as yf, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#testComment
def portfolioReport(portfolio):

    sender_email = "maxonchik.development@gmail.com"

    # Set a header to messeges

    text = """\
        Dear Mr. Shtekhno,

        Here is the performance of your portfolio by the results of today's trading: \n
        """
    html = """\
        <html>
          <body>
            <p>Dear Mr. Shtekhno,</p><br>
               Here is the performance of your portfolio by the results of today's trading: <br> \n
        """

    for email, stocks in portfolio.items():

        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = email

        for stock, amount in stocks.items():

            # Get the stock Infomation
            stockData = yf.Ticker(stock)

            # Save Data to the Variable
            stockInfo = stockData.info

            # Set the Vars with a necessary data about each ETF
            # Мне нужны: longName - полное имя, regularMarketOpen - цена на открытии, regularMarketDayHigh - топ за день, regularMarketDayLow - минимум за день
            # regularMarketPrice - цена сейчас, если ее запросить после 17, то это будет цена окончания дня

            name = stockInfo['shortName']
            currency = stockInfo['currency']

            portfolioValueOpen = round(amount * stockInfo['regularMarketOpen'], 2)
            portfolioValueCurrent = round(amount * stockInfo['regularMarketPrice'], 2)
            portfolioValueTop = round(amount * stockInfo['regularMarketDayHigh'], 2)
            portfolioValueLow = round(amount * stockInfo['regularMarketDayLow'], 2)

            diff = round(portfolioValueCurrent - portfolioValueOpen, 2)
            diffInProc = round((portfolioValueCurrent-portfolioValueOpen)/portfolioValueOpen * 100, 2)

            # Message

            list_With_good_days = ['Sir, it was a good day in the market today!', 'You are a little richer today, sir!',
                                   'I wish there were more days like this on the market, sir!']
            list_With_bad_days = ['Sir, why do you need these stocks at all?', 'Screw these stocks, sir!',
                                  'Yeah, there are better days', 'Yeah, that sucks']

            if diff >= 0:
                message["Subject"] = random.choice(list_With_good_days)
            else:
                message["Subject"] = random.choice(list_With_bad_days)

            portfolioInfoPlain = """\
            The current performance of {} in your portfolio is {} {}.
            The difference from the previous day is {} {} which is a change of {}%.
            The best price for today was {} {} and the worst {} {}.""".format(name, portfolioValueCurrent, currency, diff, currency, diffInProc, portfolioValueTop, currency, portfolioValueLow, currency)

            text += portfolioInfoPlain

            portfolioInfoHTML = """\
               The current performance of <b>{}</b> in your portfolio is <b>{} {}</b>.
               The difference from the previous day is <b>{} {}</b> which is a change of <b>{}%</b>. <br>
               The best price for today was {} {} and the worst {} {}. <br>
               <br>""".format(name, portfolioValueCurrent, currency, diff, currency, diffInProc, portfolioValueTop, currency, portfolioValueLow, currency)

            html += portfolioInfoHTML

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