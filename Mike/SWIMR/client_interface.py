'''
Created on Feb 13, 2013

@author: Mike
'''
import os
import sys
sys.path.append('../PacketStructure')
sys.path.append('../EthernetCommunication')
sys.path.append('../SerialCommunication')


from swim_client import SwimClient
from swim_packet import SwimPacket
from swim_serial import SwimSerial
import threading
import time
import string


class ClientInterface(threading.Thread):
    '''
    classdocs
    '''
    
    
    def __init__(self, host = str(), port = int()):
        threading.Thread.__init__(self)
        if host == "":
            self.IP = "153.106.75.171"
        else:
            self.HOST = host
        
        if port is None:
            self.PORT = 9999
        else:
            self.PORT = port
        
        
        self.PAYLOAD = 'DEFAULT'
                        
    def run(self):
        while 1:
            try:
                ########setup()#########
                
                #Setting up Ethernet Communication
                print 'finding server....'
                ethernet = SwimClient(self.IP,self.PORT)
                print 'server found......'
                print 'starting receive thread'
                ethernet.start()
                ############
                #########################
                
                
                ############loop()#######
                #main loop of the program
                while ethernet.ISCONNECTED:
                    time.sleep(0.2)
                    ethernet.setpayload(self.PAYLOAD)
                    ethernet.send()
                    if ethernet.ISCONNECTED:
                        print "still connected"
                    else:
                        print 'not connected!'
                        
                    if ethernet.NEWMESSAGE:
                        print "this is a new message: " + ethernet.getreceive()
                    else:
                        print 'this is not a new message: ' + ethernet.getreceive()
                ######################### 
                 
                 
                 
                ###########cleanup()#####
                #Things in this section are called if something goes wrong in loop()
                print "cleaning up"
                ethernet.cleanup()
                print 'cleaned up!'
                ########################
            except KeyboardInterrupt:
                print "bye bye"
                exit(0)
        