

import sys, os


add_to_path = sys.path.append
path_join = os.path.join
mydirname = os.path.dirname(__file__)
if sys.platform is 'linux2' or 'darwin':
    add_to_path(path_join(mydirname,'PacketStructure'))
    add_to_path(path_join(mydirname,'EthernetCommunication'))
    add_to_path(path_join(mydirname,'SerialCommunication'))
else:
    print 'unsupported os!'
    exit(1)





from swim_server import SwimServer
from swim_packet import SwimPacket
from swim_serial import SwimSerial
import time



###############Welcome################
name  = str(sys.argv[0])
print "starting {0}......".format(name)
##################################################



ethernetconnected = False
serialconnected = False

while 1:
    try:
        ########setup()#########
        if not ethernetconnected:
            #Setting up Ethernet Communication
            print 'finding client....'
            ethernet = SwimServer(9999)
            ethernet.TIMEOUT = 10.0
            print 'client found......'
            print 'starting receive thread'
            ethernet.start()
            ###########
                    
        if not serialconnected:        
            print 'connecting arduino'
            serial = SwimSerial(38400)
            serial.start()
            print 'connected!'
            ############
        #########################
        
        
        
        
        
        
        ############loop()#######
        #main loop of the program
        #while ethernet.ISCONNECTED and serial.IS_CONNECTED:
        while ethernet.ISCONNECTED and serial.IS_CONNECTED:
            ethernetconnected = ethernet.ISCONNECTED
            print "still connected"
            
            if serial.NEWMESSAGE:
                ethernet.setpayload(serial.getreceive())
                ethernet.send()
            else:
                ethernet.setpayload('PING')
                ethernet.send()
            
            if ethernet.NEWMESSAGE:
                print ethernet.RECEIVE
                serial.setpayload(ethernet.getreceive())
                serial.write()
            
                
        ########################
        
        ###########cleanup()#####
        #Things in this section are called if something goes wrong in loop()
        print 'not connected'
        if not ethernet.ISCONNECTED:
            ethernet.cleanup()  
            ethernetconnected = ethernet.ISCONNECTED
        if not serial.IS_CONNECTED:
            print 'arduino broke'
            serialconnected = serial.IS_CONNECTED
        ########################
    except KeyboardInterrupt:
        print "bye bye"
        exit(0)