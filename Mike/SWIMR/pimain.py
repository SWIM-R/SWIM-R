

import sys
sys.path.append('../SWIMR/PacketStructure')
sys.path.append('../SWIMR/EthernetCommunication')
sys.path.append('../SWIMR/SerialCommunication')





from swim_server import SwimServer
from swim_packet import SwimPacket
from swim_serial import SwimSerial
import time



###############Welcome################
name  = str(sys.argv[0])
print "starting {0}......".format(name)
##################################################



FIRSTTIME = True

while 1:
    try:
        ########setup()#########
        if FIRSTTIME:
            #Setting up Ethernet Communication
            print 'finding client....'
            ethernet = SwimServer(9999)
            print 'client found......'
            print 'starting receive thread'
            ethernet.start()
            ###########
                    
        
            #Setting up Serial Communication
            print 'connecting arduino'
            # serial = SwimSerial(38400)
            print 'connected!'
            ############
        #########################
        
        
        
        
        
        
        ############loop()#######
        #main loop of the program
        #while ethernet.ISCONNECTED and serial.IS_CONNECTED:
        while ethernet.ISCONNECTED:
            print "still connected"
            time.sleep(0.2)
            ethernet.setpayload('test')
            ethernet.send()
                
            if ethernet.NEWMESSAGE:
                print "this is a new message: " + ethernet.getreceive()
            else:
                print 'this is not a new message: ' + ethernet.getreceive()
                
        ########################
        
        ###########cleanup()#####
        #Things in this section are called if something goes wrong in loop()
        ethernet.cleanup()  
        ########################
    except KeyboardInterrupt:
        print "bye bye"
        exit(0)