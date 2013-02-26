'''
Created on Feb 25, 2013

@author: Mike
'''

#!/usr/bin/python
# The idea behind this script is if plugging a RaspberryPi into a foreign network whilst running it headless
# (i.e. without a monitor/TV), you need to know what the IP address is to SSH into it.
#
# This script emails you the IP address if it detects an ethernet address other than it's usual address
# that it normally has, i.e. on your home network.  


import subprocess
import smtplib
import string
import time

FIXED_IP = '10.10.2.10'

ipaddr_string = 'ip -4 addr > /home/pi/Desktop/SWIM-R/Mike/SWIMR/current_ip.txt'
subprocess.call(ipaddr_string, shell=True)

ip_file = file('current_ip.txt', 'r')
for line in ip_file:
    if 'eth0:' in line:
        inet_line = ip_file.next()
        _time = time.asctime()
        inet_string = inet_line[9:(inet_line.index('/'))]
   
        if inet_string != FIXED_IP:
            print 'Found eth0: %s' % inet_string
        
            SUBJECT = 'IP Address from Raspberry Pi at: %s' % time.asctime()
            TO = 'mike.capozzoli@gmail.com'
            FROM = 'mike.capozzoli@gmail.com'
            text = 'The IP address is: %s' % inet_string
            BODY = string.join((
                     'From: %s' % FROM,
                 'To: %s' % TO,
                 'Subject: %s' % SUBJECT,
                 '',
                 text
                 ), '\r\n')
        
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)     # NOTE:  This is the GMAIL SSL port.
            server.login('mike.capozzoli@gmail.com', '')
            server.sendmail(FROM, [TO], BODY)
            server.quit()

ip_file.close()

# enable the following 2 lines to delete the text file afterwards, i.e. to make it a bit cleaner.
#_string = 'rm -f ~/current_ip.txt'
#subprocess.call(_string, shell=True)
