import smtplib, ssl

def sendEmail (receiver_email, message):

    # E-Mail Settings
    port = 587  # For SSL
    smtp_server = "smtp.gmail.com"

    # Developer Account
    sender_email = "maxonchik.development@gmail.com"
    password = 'wasPif-qundyg-3tojsy'

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Setup the server variable first
    server = smtplib.SMTP(smtp_server, port)

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print('Error while setting up the connection')
        print(e)
    finally:
        server.quit()