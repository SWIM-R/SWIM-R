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
    
    
    def __init__(self, host = str(), port = int(),testing = bool()):
        threading.Thread.__init__(self)
        self.daemon = True
        self.packet = SwimPacket()
        if host == "":
            self.IP = "153.106.75.171"
        else:
            self.IP = host
        
        if port == 0:
            self.PORT = 9999
        else:
            self.PORT = port
        self.TESTING = testing
        self.ethernet = SwimClient(self.IP,self.PORT, self.TESTING)
        self.NEWMESSAGETOSEND = False
        self.PAYLOAD = 'DEFAULT'
        self.PING = 'PING'
    def run(self):
        while not self.TESTING:
            ########setup()#########
            
            #Setting up Ethernet Communication
            print 'finding server....'
            self.ethernet = SwimClient(self.IP,self.PORT,self.TESTING)
            self.ethernet.TIMEOUT = 10.0
            print 'server found......'
            print 'starting receive thread'
            self.ethernet.start()
            ############
            #########################
            
            
            ############loop()#######
            #main loop of the program
            while self.ethernet.ISCONNECTED:
                time.sleep(0.1)
                print "still connected"
                
                if self.NEWMESSAGETOSEND:
                    self.updatepayload()
                    self.ethernet.setpayload(self.PAYLOAD)
                    self.ethernet.send()
                    self.NEWMESSAGETOSEND = False
                else:
                    self.ethernet.setpayload(self.PING)
                    self.ethernet.send()
                
                if self.ethernet.NEWMESSAGE:
                    print "this is a new message from RPI: " + self.ethernet.getreceive()
                else:
                    print 'this is not a new message from RPI: ' + self.ethernet.getreceive()
                    
            ######################### 
             
             
             
            ###########cleanup()#####
            #Things in this section are called if something goes wrong in loop()
            print 'disconnected!!'
            print "cleaning up"
            self.ethernet.cleanup()
            print 'cleaned up!'
            ########################
    
    
    def updatepayload(self):
        self.PAYLOAD = str(self.packet.__dict__)
        
    def getconnectionstatus(self):
        return self.ethernet.ISCONNECTED
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
                
            clientinterface = ClientInterface(IP,PORT,False)
            clientinterface.run()
            
        except KeyboardInterrupt:
            print "bye bye"
            exit(0)
    
    
    
    
    
    
    
    
