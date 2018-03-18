import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from product.credentials import login, password


def send_email(name, subtotal, products):
    # me == my email address
    # you == recipient's email address
    me = "zender991@gmail.com"
    you = "zender991@gmail.com"

    LOGIN = login
    PASSWORD = password

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Korolchuk Geekhub Store"
    msg['From'] = me
    msg['To'] = you



    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = """\
    <html>
     <head></head>
     <body>
       <p>Hi """ + str(name) + """<br>
       <p>Homework 14 by Oleksandr Korolchuk</p>
       <p>Your products</p>
       """ + products + """
       <h4> Your subtotal - """ + str(subtotal) + """</h4>
     </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    # re-identify ourselves as an encrypted connection
    s.ehlo()
    s.login(LOGIN, PASSWORD)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()