"""
http://stackoverflow.com/questions/6270782/sending-email-with-python
"""

# Import smtplib for the actual sending function
import smtplib
import socket
import getpass

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_email(subject:str, body:str):
    # Create a text/plain message
    msg = MIMEText(body)
    hostname = socket.gethostname()
    username = getpass.getuser()
    msg['Subject'] = '[{0}]{1}'.format(hostname, subject) 
    me = msg['From'] = '{0}@{1}'.format(username, hostname)
    you = msg['To'] = '{0}@{1}'.format(username, hostname)
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(me, [you], msg.as_string())
    smtp.quit()