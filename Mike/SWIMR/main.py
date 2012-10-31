'''
Created on Oct 17, 2012

@author: Mike
'''

from swim_serial import SwimSerial

s = SwimSerial(baudrate = 9600)



while True:
    s.setpayload('bbbb')
    s.write()
    s.read()

    print s.getreceive()