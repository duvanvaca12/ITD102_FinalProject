#!/usr/bin/env python
# modified from http://elinux.org/RPi_Email_IP_On_Boot_Debian
import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import urllib
import datetime

# Change to your own account information

def run_ipscript():
    to = 'Recipient Email'
    gmail_user = 'Gmail User'
    gmail_password = 'Gmail Password'
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_password)
    today = datetime.date.today()
    # Very Linux Specific
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    get_ip = split_data[split_data.index(b'src')+1]
    ipaddr= get_ip.decode('ascii')
    my_ip = 'Server: %s:5000' %  (ipaddr)
    msg = MIMEText(my_ip)

    # # IF You want to change the body of the email.

    msg['Subject'] = 'Control car server'
    msg['From'] = gmail_user
    msg['To'] = to
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    smtpserver.quit()



