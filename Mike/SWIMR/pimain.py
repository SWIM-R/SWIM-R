

import sys
sys.path.append('../SWIMR/PacketStructure')
sys.path.append('../SWIMR/EthernetCommunication')
sys.path.append('../SWIMR/SerialCommunication')





from swim_server import SwimServer
from swim_packet import SwimPacket
from swim_serial import SwimSerial




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
            ethernet.setpayload(raw_input("What: "))
            ethernet.send()
            if ethernet.ISCONNECTED:
                print "still connected"
            else:
                print 'not connected!'
                
        #########################  
        
        
        
        
        ###########cleanup()#####
        #Things in this section are called if something goes wrong in loop()
        ethernet.stopreceivethread = True  
        ethernet.SOCK.close()  
        ethernet.__stop()
        ########################
    except KeyboardInterrupt:
        print "bye bye"
        exit(0)