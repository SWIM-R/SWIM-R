'''
Created on Oct 31, 2012

@author: Mike
'''
import socket
#import sys
#data = "test".join(sys.argv[1:])


class SwimClient():
    '''
    classdocs
    '''
    def __init__(self, host = str(), port = int() ):
        '''
        Constructor
        '''
        
        if host == "":
            self.HOST = "153.106.113.58"
        else:
            self.HOST = host
        
        if port is None:
            self.PORT = 9999
        else:
            self.PORT = port
            
        self.PAYLOAD = "default"
        self.RECEIVE = ''

        self.initialize()

    def initialize(self):
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send(self):
        self.SOCK.sendto(self.PAYLOAD + "\n", (self.HOST, self.PORT))
        
    def setpayload(self, payload):
        self.PAYLOAD = payload
        
    def getreceive(self):
        return self.RECEIVE
    
    def receive(self, size = int()):
        self.RECEIVE = self.SOCK.recv(size)

        





