'''
Created on Oct 17, 2012

@author: Mike
'''


from swim_client import SwimClient


#message = 'bbbb'
#s = SwimSerial(baudrate = 9600)
C = SwimClient(host = '169.254.6.123', port = 9999)

while True:
    C.setpayload('gimme')
    C.send()
    
    C.receive(4096)
    d = C.getreceive()
    print d







#    if(s.IS_CONNECTED):
#        s.setpayload(message)
#        s.write()
#        s.read()
#        b = s.getreceive()
#        print b
#    else:
#        s.initialize()
#        print 'not connected'