'''
Created on Jan 10, 2013

@author: Mike
'''
import socket
class SwimServer(object):
    '''
    classdocs
    '''
    def __init__(self,PORT = int()):
        #initialize a UDP socket
        
        # Listen on port PORT
        # (to all IP addresses on this system)
        self.ISCONNECTED = False
        self.RECEIVE = str()
        self.PAYLOAD = str()
        
        if PORT is None:
            PORT = 9999
        
        self.initialize(PORT)
        
    def initialize(self,PORT):
        self.SOCK = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        #Listen to all IPs on system
        listen_addr = ("",PORT)
        self.SOCK.bind(listen_addr)
    
    def getreceive(self):
        return self.RECEIVE
    def getpayload(self):
        return self.PAYLOAD
    def setpayload(self,payload = str()):
        self.PAYLOAD = payload
    def send(self):
        if len(self.PAYLOAD)<=8192 and len(self.PAYLOAD)>0:
            self.SOCK.sendto(self.PAYLOAD,(self.HOST,self.PORT))
            self.SOCK.sendto('Done',(self.HOST,self.PORT))
        else:
            self.SOCK.sendto(self.PAYLOAD[:8192], (self.HOST,self.PORT))
            self.helpersend(self.PAYLOAD[8192:])
            
    def helpersend(self,payload):
        if len(payload)<=8192 and len(payload)>0:
            self.SOCK.sendto(payload,(self.HOST,self.PORT))
            self.SOCK.sendto('Done',(self.HOST,self.PORT))
        else:
            self.SOCK.sendto(payload[:8192], (self.HOST,self.PORT))
            self.helpersend(payload[8192:])
        
   
    def receive(self,size = int()):
        self.RECEIVE = ''
        receivedstring = self.SOCK.recv(size)
        while 1:
            self.RECEIVE = self.RECEIVE + receivedstring
            receivedstring = self.SOCK.recv(size)
            if receivedstring == 'done':
                break    


if __name__ == "main":
    print "main"
    
    c = SwimServer(9999)
    while 1:
        shit = raw_input("what?: ")
        c.setpayload(shit)
        c.send
    
    
else: print "not main"
