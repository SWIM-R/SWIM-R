'''
Created on Oct 31, 2012

@author: Mike
'''
import socket
#import sys
#data = "test".join(sys.argv[1:])


class SwimClient(object):
    '''
    classdocs
    '''
    def __init__(self, host = str(), port = int() ):
        '''
        Constructor
        '''
        
        if host == "":
            self.HOST = "153.106.75.171"
        else:
            self.HOST = host
        
        if port is None:
            self.PORT = 9999
        else:
            self.PORT = port
            
        self.PAYLOAD = "default"
        self.RECEIVE = ''
        self.ISCONNECTED = False
        self.HOSTPORT = (self.HOST, self.PORT)
        self.initialize()

    def initialize(self):
        '''
        initializes 
        '''
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #Find the server
        self.setpayload("Hello!")
        while 1:
            self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)

            data, addr = self.SOCK.recvfrom(1024)
            print data
            print data.strip()
            if data.strip() == 'hello client':
                print"I've found the server"
                self.ISCONNECTED == True
                break
        
        
    def send(self):
        if len(self.PAYLOAD)<=8192 and len(self.PAYLOAD)>0:
            self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
            self.SOCK.sendto('Done',(self.HOST,self.PORT))
        else:
            self.SOCK.sendto(self.PAYLOAD[:8192], self.HOSTPORT)
            self.helpersend(self.PAYLOAD[8192:])
            
            #self.SOCK.sendto(self.PAYLOAD + "\n", (self.HOST, self.PORT))
    def helpersend(self,payload):
        if len(payload)<=8192 and len(payload)>0:
            self.SOCK.sendto(payload,self.HOSTPORT)
            self.SOCK.sendto(payload, self.HOSTPORT)
        else:
            self.SOCK.sendto(payload[:8192], self.HOSTPORT)
            self.helpersend(payload[8192:])
        
    def setpayload(self, payload):
        self.PAYLOAD = payload
        
    def getreceive(self):
        return self.RECEIVE
    
    def receive(self, size = int()):
        self.RECEIVE = ''
        receivedstring = self.SOCK.recv(size)
        while receivedstring != "done":
            self.RECEIVE = self.RECEIVE + receivedstring
            receivedstring = self.SOCK.recv(size)
            if receivedstring == 'done':
                break
        

if __name__=='__main__':
    #from swim_client import SwimClient
    import sys
    
    try:
        IP,PORT = str(sys.argv[1]),int(sys.argv[2])
    except:
        print" you forgot command line arguments stupid"
        exit(1)
    c = SwimClient(IP,PORT)

    while 1:
        shit = raw_input("what?: ")
        c.setpayload(shit)
        c.send()
        c.receive(1024)
        print "RPi says: " + c.getreceive()


