# Import smtplib to provide email functions
import smtplib
import ConfigParser
import mail_template
  
# Import the email modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = ConfigParser.ConfigParser()
config.read("/etc/thermvis/thermvis.conf")
smtp_server = config.get('SMTP', 'SmtpServer')
smtp_port   = config.getint('SMTP','SmtpPort')
smtp_user   = config.get('SMTP','Username')
smtp_pass   = config.get('SMTP','Password')

# Define email addresses to use
addr_to   = 'domi94@gmx.ch'
addr_from = 'thermvis@raspi.com'
  
# Construct email
msg = MIMEMultipart('alternative')
msg['To'] = addr_to
msg['From'] = addr_from
msg['Subject'] = 'Test Email From RPi'

# Get the body of the message and substitute variables.
html = mail_template.html.format(**locals())

# Record the MIME types of both parts - text/plain and text/html.
part = MIMEText(html, 'html')
  
# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part)
  
# Send the message via an SMTP server
try:
  s = smtplib.SMTP(smtp_server, smtp_port)
  s.ehlo()
  s.starttls()
  s.login(smtp_user,smtp_pass)
  s.sendmail(addr_from, addr_to, msg.as_string())
  s.quit()
except:
  print("There was an error sending the email. Check the smtp settings.")
