'''
Created on Jan 10, 2013

@author: Mike
'''
import socket
from socket import error
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
        self.MAXPACKETSIZE = 32
        
        if PORT is None:
            PORT = 9999
        
        self.initialize(PORT)
        
    def initialize(self,PORT):
        self.SOCK = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
       
        #no blocking!
        self.SOCK.setblocking(0)
        #Listen to all IPs on system
        listen_addr = ("",PORT)
        self.SOCK.bind(listen_addr)
        
        #find the client computer
        while self.ISCONNECTED == False:
            try:
                self.RECEIVE, self.CLIENTIP = self.SOCK.recvfrom(1024)
            except error:
                continue
            print "This This is client IP and message: ",self.RECEIVE, self.CLIENTIP
            if self.CLIENTIP is not None:
                self.ISCONNECTED = True
                self.SOCK.sendto("hello client",self.CLIENTIP)
                #self.SOCK.sendall("hello client",)
                break
            
        print "I've found the client"
    
    def getreceive(self):
        return self.RECEIVE
    def getpayload(self):
        return self.PAYLOAD
    def setpayload(self,payload = str()):
        self.PAYLOAD = payload
    def send(self):
        if len(self.PAYLOAD)<=self.MAXPACKETSIZE and len(self.PAYLOAD)>0:
            self.SOCK.sendto(self.PAYLOAD,self.CLIENTIP)
            self.SOCK.sendto('done',self.CLIENTIP)
        else:
            self.SOCK.sendto(self.PAYLOAD[:self.MAXPACKETSIZE], self.CLIENTIP)
            self.helpersend(self.PAYLOAD[self.MAXPACKETSIZE:])
            
    def helpersend(self,payload):
        if len(payload)<=self.MAXPACKETSIZE and len(payload)>0:
            self.SOCK.sendto(payload,self.CLIENTIP)
            self.SOCK.sendto('done',self.CLIENTIP)
        else:
            self.SOCK.sendto(payload[:self.MAXPACKETSIZE],self.CLIENTIP)
            self.helpersend(payload[self.MAXPACKETSIZE:])
   
    def receive(self,size = int()):
        self.RECEIVE = ''
        receivedstring = str()
        while 1:
            try:
                receivedstring = self.SOCK.recv(size)
            except:
                continue
            if receivedstring == 'done':
                break
            else:
                self.RECEIVE = self.RECEIVE + receivedstring
            

if __name__ == '__main__':
    print "main"
    print 'serving'
    c = SwimServer(9999)
    while 1:
        c.receive(1024)
        c.setpayload(c.getreceive())
        c.send()
    
