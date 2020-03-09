# This file should handle sending emails to address specified somewhere

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import asctime

# password = input("Pls giff password: ")
# set up the SMTP server
s = smtplib.SMTP(host='owa.ist.ac.at', port=587)
s.starttls()
# s.login("ldrmic", password=password)

msg = MIMEMultipart()
msg["From"] = "luka.drmic@ist.ac.at"
msg["To"] = "luka.drmic@ist.ac.at"
msg["Subject"] = "This is a test msg for pump alert"

instrument = "Pump 1 monitor"
temp = "45.6"

msg_content = "Time: {}\nInstrument: {}\nTemperature: {}".format(asctime(), instrument, temp)

msg.attach(MIMEText(msg_content, "plain"))
print(msg)
# s.send_message(msg)