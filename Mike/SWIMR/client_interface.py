'''x
Created on Feb 13, 2013

@author: Mike
'''
import os
import sys

add_to_path = sys.path.append
path_join = os.path.join
mydirname = os.path.dirname(__file__)

if sys.platform == 'win32' or 'cli':
    add_to_path(path_join(mydirname,'PacketStructure'))
    add_to_path(path_join(mydirname,'EthernetCommunication'))
    add_to_path(path_join(mydirname,'SerialCommunication'))
    add_to_path(path_join(mydirname, 'VideoStreaming'))
elif sys.platform == 'darwin' or sys.platform == 'linux2':
    add_to_path(path_join(mydirname,'PacketStructure'))
    add_to_path(path_join(mydirname,'EthernetCommunication'))
    add_to_path(path_join(mydirname,'SerialCommunication'))
    add_to_path(path_join(mydirname, 'VideoStreaming'))
else:
    print 'unsupported os!'

#from swim_video_client import SwimVideoClient
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
        self.PAYLOAD = self.packet.__dict__
        self.PING = 'PING'
        self.READ_DATAFORMAT = 'ERROR', 'ROLL','PITCH','YAW','WATER_TEMPERATURE','CASE_TEMPERATURE', 'DEPTH', 'BATTERY', 'HUMIDITY' # the format that should come from the Arduino
        self.RECEIVE = {'ERROR': 0 , 'ROLL' : 0 , 'PITCH': 0,'YAW': 0,'WATER_TEMPERATURE':0,'CASE_TEMPERATURE': 0,'DEPTH': 0, 'BATTERY':0 ,'HUMIDITY': 0}
        self.BEFOREFIRSTARMED = True
        self.SENSORDATA = self.RECEIVE
        if not self.TESTING:
            self.start()
    def run(self):
        self.ethernet = SwimClient(self.IP,self.PORT,False) 
        #self.video = SwimVideoClient(360,480,5) # length, width, framerate
        try:    
            while not self.TESTING:     
                time.sleep(0.055)            
                ############loop()#######
                #main loop of the program
                if self.ethernet.ISCONNECTED:
                    #time.sleep(0.5)                    
                    if not self.BEFOREFIRSTARMED:
                        if self.NEWMESSAGETOSEND:
                            self.NEWMESSAGETOSEND = False
                            self.updatepayload()
                            self.ethernet.setpayload(self.PAYLOAD)
                            self.ethernet.send()
                        else:
                            self.ethernet.setpayload('PING')
                            self.ethernet.send()
                    else:
                        neutral_packet = SwimPacket()
                        self.ethernet.setpayload(str(neutral_packet.__dict__))
                        self.ethernet.send()
                    
                    if self.ethernet.NEWMESSAGE:
                        try:
#                            tempdict = ast.literal_eval(self.ethernet.getreceive())
                            self.RECEIVE = ast.literal_eval(self.ethernet.getreceive())
                            print self.RECEIVE
                            self.updatesensordata()
#                            if tempdict.has_key('str'):
#                                self.video.set_frame(tempdict)
#                                print "received frame!!"
#                            else:
#                                self.RECEIVE = tempdict
                        except Exception as e:#see what happened
                            print e
                if self.ethernet.ISCONNECTED is False:   
                    print 'disconnected!!'
                    print "cleaning up"
                    self.BEFOREFIRSTARMED = True
                    self.ethernet.cleanup()
                    print 'cleaned up!'
                    self.ethernet = SwimClient(self.IP,self.PORT,False) 
        except:
            self.ethernet.ISCONNECTED = False
            ########################
    
    
    def updatepayload(self):
        self.PAYLOAD = str(self.packet.__dict__)
    
    def updatesensordata(self):
        
        for key in self.READ_DATAFORMAT:
            try:
                self.SENSORDATA[key] = self.RECEIVE[key]
            except:
                continue
    def getconnectionstatus(self):
        if self.ethernet is not None:
            return self.ethernet.ISCONNECTED
        else:
            return False
    def setARM(self,arm = bool()):
        if self.packet.ARM is not arm:
            self.packet.PITCH = 127
            self.packet.ROLL = 127
            self.packet.YAW = 127
            self.packet.X = 127
            self.packet.Y = 127
            self.packet.Z = 127 
        self.BEFOREFIRSTARMED = False   
        self.packet.ARM = arm        
        self.NEWMESSAGETOSEND = True
    def getpacket(self):
        return self.packet.__dict__
    def setX(self,x = int()):
        if self.packet.ARM:    
            if x > 255:
                x = 255
            elif x < 0:
                x = 0
            else:
                pass
            self.packet.X = x
            self.NEWMESSAGETOSEND = True
    
    def setY(self,y = int()):
        if self.packet.ARM:
            if y > 255:
                y = 255
            elif y < 0:
                y = 0
            else:
                pass
            self.packet.Y = y
            self.NEWMESSAGETOSEND = True

    def setZ(self,z = int()):
        if self.packet.ARM:
            if z > 255:
                z = 255
            elif z < 0:
                z = 0
            else:
                pass        
            self.packet.Z = z
            self.NEWMESSAGETOSEND = True

    def setYaw(self,yaw = int()):
        if self.packet.ARM:    
            if yaw > 255:
                yaw = 255
            elif yaw < 0:
                yaw = 0
            else:
                pass
            self.packet.YAW = yaw
            self.NEWMESSAGETOSEND = True

    def setPitch(self, pitch = int()):
        if self.packet.ARM:    
            if pitch > 255:
                pitch = 255
            elif pitch < 0:
                pitch = 0
            else:
                pass
            self.packet.PITCH = pitch
            self.NEWMESSAGETOSEND = True

    def setRoll(self,roll = int()):
        if self.packet.ARM:   
            if roll > 255:
                roll = 255
            elif roll < 0:
                roll = 0
            else:
                pass        
            self.packet.ROLL = roll
            self.NEWMESSAGETOSEND = True
        
#self.READ_DATAFORMAT ='ROLL','PITCH','YAW','WATER_TEMPERATURE','CASE_TEMPERATURE','HUMIDITY' , 'DEPTH', 'BATTERY' # the format that should come from the Arduino

    def getWaterTemperature(self):
        try:
            return self.SENSORDATA['WATER_TEMPERATURE']
        except Exception as e:
            raise e
    def getCaseTemperature(self):
        try:
            return self.SENSORDATA['CASE_TEMPERATURE']
        except Exception as e:
            raise e
    def getHumidity(self):
        try:
            return self.SENSORDATA['HUMIDITY']
        except Exception as e:
            raise e
    def getBatteryLife(self):
        try:
            return self.SENSORDATA['BATTERY']
        except Exception as e:
            raise e
        
    def getError(self):
        '''
        returns true if the arduino connection has malfunctioned
        '''
        try:
            return self.SENSORDATA['ERROR']
        except Exception as e:
            raise e
    def getDepth(self):
        try:
            return self.SENSORDATA['DEPTH']
        except Exception as e:
            raise e
    def getRoll(self):
        try:
            return self.SENSORDATA['ROLL']
        except Exception as e:
            raise e
    def getPitch(self):
        try:
            return self.SENSORDATA['PITCH']
        except Exception as e:
            raise e
    def getYaw(self):
        try:
            return self.SENSORDATA['YAW']
        except Exception as e:
            raise e
if __name__ == '__main__':
    if sys.platform != 'win32':
        try:
            try:
                IP,PORT = str(sys.argv[1]),int(sys.argv[2])
            except:
                print "try: python clientmain.py <SERVERIP> <PORT>"
                exit(1)
                
            clientinterface = ClientInterface(IP,PORT,False)  
            while 1:
                pass          
        except KeyboardInterrupt:
            print "bye bye"
            exit(0)
    
    
    
    
    
    
    
    
