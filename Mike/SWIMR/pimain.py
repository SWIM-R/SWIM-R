

import sys, os


add_to_path = sys.path.append
path_join = os.path.join
mydirname = os.path.dirname(__file__)
if sys.platform is 'linux2' or 'darwin': #if I'm runnning on the rpi or mikes macbook, then go ahead
    add_to_path(path_join(mydirname,'PacketStructure'))
    add_to_path(path_join(mydirname,'EthernetCommunication'))
    add_to_path(path_join(mydirname,'SerialCommunication'))
else: #otherwise screw you!
    print 'unsupported os!'
    exit(1)





from swim_server import SwimServer
from swim_serial import SwimSerial
import time



###############Welcome################
name  = str(sys.argv[0])
print "starting {0}......".format(name)
##################################################



ethernetconnected = False
serialconnected = False

while 1:
    time.sleep(0.1) 

    try:
        if not serialconnected:        
            print 'connecting arduino'
            serial = SwimSerial(115200)
            print 'started receive thread...'
            serial.start()
            print 'arduino connected!'
            ############
        #########################
        
        
        ########setup()#########
        if not ethernetconnected:
            #Setting up Ethernet Communication
            print 'finding client....'
            ethernet = SwimServer(9999)
            print 'client found......'
            ethernet.start()
            
            ###########
        ############loop()#######
        #main loop of the program
        #while ethernet.ISCONNECTED and serial.ISCONNECTED:
        while ethernet.ISCONNECTED and serial.ISCONNECTED:
            time.sleep(0.1) 
            ethernetconnected = ethernet.ISCONNECTED
            serial.ETHERNETCONNECTION = ethernet.ISCONNECTED #So the serial has some idea about the state of the ethernet connection
            serialconnected = serial.ISCONNECTED
            ethernet.ARDUINOCONNECTION = serial.ISCONNECTED
            print "still connected"
            
            if serial.NEWMESSAGE: # If there is a new message from the Arduino 
                ethernet.setpayload(serial.getreceive())
                ethernet.send()
            else: #otherwise just ping
                ethernet.setpayload("{'PING': 0 }")
                ethernet.send()
            
            if ethernet.NEWMESSAGE: #if there is a new message from the Computer
                print 'new message from jon!'
                serial.setpayload(ethernet.getreceive())
                print ethernet.getreceive()
                #serial.write()
            else: #just send the old packet again
                #serial.write()
                pass
                
        ########################
        
        ###########cleanup()#####
        #Things in this section are called if something goes wrong in loop()
        if not ethernet.ISCONNECTED or not serial.ISCONNECTED:
            if not serial.ISCONNECTED:
                print 'arduino broke'
            elif not ethernet.ISCONNECTED:
                print 'ethernet broke'            
            ethernetconnected = ethernet.ISCONNECTED
            serial.ETHERNETCONNECTION = ethernet.ISCONNECTED
            ethernet.ARDUINOCONNECTION = serial.ISCONNECTED
            serialconnected = serial.ISCONNECTED  
            serial.cleanup()
            ethernet.cleanup()                      
        ########################
    except KeyboardInterrupt:
        print "bye bye"
        exit(0)
    except Exception as e:
        with open('/Users/Mike/Desktop/errorlog.txt','a') as f:
            f.write(str(e)+'\n')