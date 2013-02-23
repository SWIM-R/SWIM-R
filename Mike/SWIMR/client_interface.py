'''
Created on Feb 13, 2013

@author: Mike
'''
import os
import sys

add_to_path = sys.path.append
path_join = os.path.join
mydirname = os.path.dirname(__file__)

if sys.platform is 'darwin' or 'win32':
    add_to_path(path_join(mydirname,'PacketStructure'))
    add_to_path(path_join(mydirname,'EthernetCommunication'))
    add_to_path(path_join(mydirname,'SerialCommunication'))

else:
    print 'unsupported os!'
    exit(1)

from swim_client import SwimClient
from swim_packet import SwimPacket
from swim_serial import SwimSerial
import threading
import time


class ClientInterface(threading.Thread):
    '''
    classdocs
    '''
    
    
    def __init__(self, host = str(), port = int()):
        threading.Thread.__init__(self)
        self.daemon = True
        self.packet = SwimPacket()
        if host == "":
            self.IP = "153.106.75.171"
        else:
            self.IP = host
        
        if port is None:
            self.PORT = 9999
        else:
            self.PORT = port
        
        self.NEWMESSAGETOSEND = False
        self.PAYLOAD = 'DEFAULT'
        self.PING = 'PING'
    def run(self):
        while 1:
            ########setup()#########
            
            #Setting up Ethernet Communication
            print 'finding server....'
            ethernet = SwimClient(self.IP,self.PORT)
            ethernet.TIMEOUT = 10.0
            print 'server found......'
            print 'starting receive thread'
            ethernet.start()
            ############
            #########################
            
            
            ############loop()#######
            #main loop of the program
            while ethernet.ISCONNECTED:
                print "still connected"

                time.sleep(0.2)
                if self.NEWMESSAGETOSEND:
                    self.updatepayload()
                    ethernet.setpayload(self.PAYLOAD)
                    ethernet.send()
                    self.NEWMESSAGETOSEND = False
                else:
                    ethernet.setpayload(self.PING)
                    ethernet.send()
                
                if ethernet.NEWMESSAGE:
                    print "this is a new message: " + ethernet.getreceive()
                else:
                    print 'this is not a new message: ' + ethernet.getreceive()
                    
            ######################### 
             
             
             
            ###########cleanup()#####
            #Things in this section are called if something goes wrong in loop()
            print 'disconnected!!'
            print "cleaning up"
            ethernet.cleanup()
            print 'cleaned up!'
            ########################
    
    
    def updatepayload(self):
        self.PAYLOAD = str(self.packet.__dict__)
        
    def setX(self,x = int()):
        self.packet.X = x
        self.NEWMESSAGETOSEND = True
    
    def setY(self,y = int()):
        self.packet.Y = y
        self.NEWMESSAGETOSEND = True

    def setZ(self,z = int()):
        self.packet.Z = z
        self.NEWMESSAGETOSEND = True

    def setYaw(self,yaw = int()):
        self.packet.YAW = yaw
        self.NEWMESSAGETOSEND = True

    def setPitch(self, pitch = int()):
        self.packet.PITCH = pitch
        self.NEWMESSAGETOSEND = True

    def setRoll(self,roll = int()):
        self.packet.ROLL = roll
        self.NEWMESSAGETOSEND = True

    
    
if __name__ == '__main__':
    if sys.platform != 'win32':
        try:
            try:
                IP,PORT = str(sys.argv[1]),int(sys.argv[2])
            except:
                print "try: python clientmain.py <SERVERIP> <PORT>"
                exit(1)
                
            clientinterface = ClientInterface(IP,PORT)
            clientinterface.run()
            
        except KeyboardInterrupt:
            print "bye bye"
            exit(0)
    
    
    
    
    
    
    
    