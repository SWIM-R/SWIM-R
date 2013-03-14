

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
    time.sleep(0.5) 

    try:
        if not serialconnected:        
            print 'connecting arduino'
            serial = SwimSerial(115200)
            print 'started arduino receive thread...'
            #serial.start() #starting the receive thread
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
        while ethernet.ISCONNECTED or serial.ISCONNECTED:
            time.sleep(0.5) 
            ethernetconnected = ethernet.ISCONNECTED
            serial.ETHERNETCONNECTION = ethernet.ISCONNECTED #So the serial has some idea about the state of the ethernet connection
            serialconnected = serial.ISCONNECTED
            ethernet.ARDUINOCONNECTION = serial.ISCONNECTED
            print "still connected"
            
            if serial.ISCONNECTED:
                if serial.NEWMESSAGE: # If there is a new message from the Arduino 
                    ethernet.setpayload(serial.getreceive())
                    ethernet.send()
                else: #otherwise just ping
                    ethernet.setpayload("{'PING': 0 }")
                    ethernet.send()
            else: #ping the error message
                ethernet.setpayload("{'PING': 0 }")
                ethernet.send()
                
            if ethernet.ISCONNECTED:
                if ethernet.NEWMESSAGE: #if there is a new message from the Computer
                    print 'new message from jon!'
                    print ethernet.getreceive()
                    serial.setpayload(ethernet.getreceive())
                    serial.write()
                else: #just send the old packet again
                    serial.write()
            else:
                serial.write()
                
        ########################
        
            ###########cleanup()#####
            #Things in this section are called if something goes wrong in loop()
            if not ethernet.ISCONNECTED or not serial.ISCONNECTED:
                ethernetconnected = ethernet.ISCONNECTED
                serial.ETHERNETCONNECTION = ethernet.ISCONNECTED #So the serial has some idea about the state of the ethernet connection
                serialconnected = serial.ISCONNECTED
                ethernet.ARDUINOCONNECTION = serial.ISCONNECTED  
                if not serial.ISCONNECTED:
                    serial.cleanup()
                    print 'arduino broke'
                    break
                if not ethernet.ISCONNECTED:
                    print 'ethernet broke'  
                    ethernet.cleanup()
                    break
                  
            ########################
    except KeyboardInterrupt:
        print "bye bye"
        exit(0)
    except Exception as e:
        with open('/Users/Mike/Desktop/errorlog.txt','a') as f:
            f.write(str(e)+'\n')