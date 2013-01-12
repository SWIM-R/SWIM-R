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
        
        #find the client computer
        while self.ISCONNECTED == False:
                self.RECEIVE, self.CLIENTIP = self.SOCK.recvfrom(1024)
                if self.CLIENTIP is not None:
                    self.ISCONNECTED == True
                    self.SOCK.sendto("hello client",self.CLIENTIP)
                    #self.SOCK.sendall("hello client",)
        print "I've found the client"
    
    def getreceive(self):
        return self.RECEIVE
    def getpayload(self):
        return self.PAYLOAD
    def setpayload(self,payload = str()):
        self.PAYLOAD = payload
    def send(self):
        if len(self.PAYLOAD)<=8192 and len(self.PAYLOAD)>0:
            self.SOCK.sendto(self.PAYLOAD,(self.CLIENTIP,self.PORT))
            self.SOCK.sendto('Done',(self.CLIENTIP,self.PORT))
        else:
            self.SOCK.sendto(self.PAYLOAD[:8192], (self.HOST,self.PORT))
            self.helpersend(self.PAYLOAD[8192:])
            
    def helpersend(self,payload):
        if len(payload)<=8192 and len(payload)>0:
            self.SOCK.sendto(payload,(self.CLIENTIP,self.PORT))
            self.SOCK.sendto('Done',(self.CLIENTIP,self.PORT))
        else:
            self.SOCK.sendto(payload[:8192], (self.CLIENTIP,self.PORT))
            self.helpersend(payload[8192:])
        
   
    def receive(self,size = int()):
        self.RECEIVE = ''
        receivedstring = self.SOCK.recv(size)
        while 1:
            self.RECEIVE = self.RECEIVE + receivedstring
            receivedstring = self.SOCK.recv(size)
            if receivedstring == 'done':
                break    


if __name__ == '__main__':
    print "main"
    print 'serving'
    c = SwimServer(9999)
    while 1:
        c.receive(1024)
        c.setpayload(c.getreceive())
        c.send()
    
