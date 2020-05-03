import smtplib, ssl
import os 
from os import path
if path.exists("env.py"):
  import env 

port = 465  # For SSL
password = os.environ.get('GMAIL_SECRET')

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("linuxcommandgen@gmail.com", password)
    print('it worked')