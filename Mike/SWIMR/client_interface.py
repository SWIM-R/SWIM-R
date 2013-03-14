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
import threading
import time
import ast

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
        self.ethernet = None
        self.NEWMESSAGETOSEND = False
        self.PAYLOAD = 'DEFAULT'
        self.PING = 'PING'
        self.READ_DATAFORMAT = 'ERROR', 'ROLL','PITCH','YAW','TEMPERATURE', 'DEPTH', 'BATTERY' # the format that should come from the Arduino
        self.RECEIVE = {'ERROR': 0 , 'ROLL' : 128 , 'PITCH': 128,'YAW': 128,'TEMPERATURE': 0,'DEPTH': 0, 'BATTERY':0}
    def run(self):
        while not self.TESTING:
            time.sleep(0.5)

            ########setup()#########
            
            #Setting up Ethernet Communication
            print 'finding server....'
            self.ethernet = SwimClient(self.IP,self.PORT,self.TESTING)
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
                    print 'ping'
                    self.ethernet.setpayload('PING')
                    self.ethernet.send()
                
                if self.ethernet.NEWMESSAGE:
                    try:
                        self.RECEIVE = ast.literal_eval(self.ethernet.getreceive())
                    except:#see what happened
                        print self.ethernet.getreceive()
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
        if x > 255:
            x = 255
        elif x < 0:
            x = 0
        else:
            pass
        self.packet.X = x
        self.NEWMESSAGETOSEND = True
    
    def setY(self,y = int()):
        if y > 255:
            y = 255
        elif y < 0:
            y = 0
        else:
            pass
        self.packet.Y = y
        self.NEWMESSAGETOSEND = True

    def setZ(self,z = int()):
        if z > 255:
            z = 255
        elif z < 0:
            z = 0
        else:
            pass        
        self.packet.Z = z
        self.NEWMESSAGETOSEND = True

    def setYaw(self,yaw = int()):
        if yaw > 255:
            yaw = 255
        elif yaw < 0:
            yaw = 0
        else:
            pass
        self.packet.YAW = yaw
        self.NEWMESSAGETOSEND = True

    def setPitch(self, pitch = int()):
        if pitch > 255:
            pitch = 255
        elif pitch < 0:
            pitch = 0
        else:
            pass
        self.packet.PITCH = pitch
        self.NEWMESSAGETOSEND = True

    def setRoll(self,roll = int()):
        if roll > 255:
            roll = 255
        elif roll < 0:
            roll = 0
        else:
            pass        
        self.packet.ROLL = roll
        self.NEWMESSAGETOSEND = True
        
#   self.READ_DATAFORMAT = 'ERROR', 'ROLL','PITCH','YAW','TEMPERATURE', 'DEPTH', 'BATTERY' # the format that should come from the Arduino

    def getTemperature(self):
        try:
            return self.RECEIVE['TEMPERATURE']
        except:
            return 0
    def getBatteryLife(self):
        try:
            return self.RECEIVE['BATTERY']
        except:
            return 0
        
    def getError(self):
        '''
        returns true if the arduino connection has malfunctioned
        '''
        try:
            return self.RECEIVE['ERROR']
        except:
            return 0
    def getDepth(self):
        try:
            return self.RECEIVE['DEPTH']
        except:
            return 0
    def getRoll(self):
        try:
            return self.RECEIVE['ROLL']
        except:
            return 0
    def getPitch(self):
        try:
            return self.RECEIVE['PITCH']
        except:
            return 0
    def getYaw(self):
        try:
            return self.RECEIVE['YAW']
        except:
            return 0
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
    
    
    
    
    
    
    
    
