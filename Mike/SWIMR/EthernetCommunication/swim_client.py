'''
Created on Oct 31, 2012

@author: Mike
'''
import socket
import threading
import time
from socket import error 
from socket import timeout
#import sys
#data = "test".join(sys.argv[1:])


class SwimClient(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self, host = str(), port = int(),testing = bool() ):
        '''
        Initializes...everything.  
        '''
        threading.Thread.__init__(self)
        
        if host == "":
            self.HOST = "153.106.75.171"
        else:
            self.HOST = host
        
        if port == 0:
            self.PORT = 9999
        else:
            self.PORT = port
            
        self.PAYLOAD = str()
        self.RECEIVE = str()
        self.ISCONNECTED = False
        self.MAXPACKETSIZE = 8196
        self.HOSTPORT = (self.HOST, self.PORT)
        self.stopreceivethread = False
        self.daemon = True
        self.TIMEOUT = 3.0
        self.NEWMESSAGE = True

        if not testing:
            self.initialize()
        
        
    def initialize(self):
        '''
        initializes connection to server, if successfully initialized sets ISCONNECTED to be true
        '''
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        #socket for sending
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
       
        # sets socket to be nonblocking, if data can't immediately be sent or received then an exception is raised
        #self.SOCK.setblocking(0)
        
        
        #sets socket to be blocking along with a timeout, if can't be sent to received within 5 seconds then the timeout exception is raised
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(self.TIMEOUT)
        
        
        #Find the server
        self.setpayload("Hello!")
        self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)

        while not self.ISCONNECTED:
            try:
                self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
                data, addr = self.SOCK.recvfrom(32)
                if data.strip() == 'hello client':
                    print"I've found the server"
                    self.ISCONNECTED = True 
                time.sleep(0.5)
            except timeout:
                continue        
    def send(self):
        '''
        sends whatever is in self.PAYLOAD. calls helpersend if it is large message.  Sends 'done' at the end of a packet
        '''
        
        if len(self.PAYLOAD) <= 0:
            return
        
        
        elif len(self.PAYLOAD)<=self.MAXPACKETSIZE:
            self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
            self.SOCK.sendto('done',(self.HOST,self.PORT))
        else:
            self.SOCK.sendto(self.PAYLOAD[:self.MAXPACKETSIZE], self.HOSTPORT)
            self.helpersend(self.PAYLOAD[self.MAXPACKETSIZE:])            
    def helpersend(self,payload):
        '''
        don't call helpersend directly.  sends 'done' at the end of a packet
        '''
        time.sleep(.001)
        if len(payload)<=self.MAXPACKETSIZE and len(payload)>0:
            self.SOCK.sendto(payload,self.HOSTPORT)
            self.SOCK.sendto('done', self.HOSTPORT)
        else:
            self.SOCK.sendto(payload[:self.MAXPACKETSIZE], self.HOSTPORT)
            self.helpersend(payload[self.MAXPACKETSIZE:])


    def setpayload(self, payload = str()):
        '''
        setter for the payload that is going to be sent 
        '''
        self.PAYLOAD = payload
        
    def getreceive(self):
        '''
        getter for whatever has been received
        '''
        self.NEWMESSAGE = False
        return self.RECEIVE
   
    
    def receive(self, size = int()):
        '''
        receives a packet until it gets 'done'.  the packet is stored in RECEIVE
        '''
        receivedstring = str()
        temp = str()
        while 1:
            try:
                receivedstring = self.SOCK.recv(size)
            except:#timeout
                self.ISCONNECTED = False
                self.stopreceivethread = True
                return
            if receivedstring == 'done':
                if temp == '':
                    continue
                else:
                    break
            elif receivedstring == 'PING':
                self.NEWMESSAGE = False
                continue
            else:
                temp = temp + receivedstring  
        self.NEWMESSAGE = True
        self.RECEIVE = temp
    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        while self.stopreceivethread == False:
            self.receive(self.MAXPACKETSIZE)
   
    def cleanup(self):
        '''
        stops closes the socket and stops the receive thread
        '''
        try:
            self.stopreceivethread = True 
            time.sleep(0.01)
            self.SOCK.shutdown(socket.SHUT_RDWR)
            self.SOCK.close()  
        except Exception as e:
            print e
    


