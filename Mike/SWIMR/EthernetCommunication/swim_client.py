'''
Created on Oct 31, 2012

@author: Mike
'''
import socket
import threading
import time
from socket import error 
#import sys
#data = "test".join(sys.argv[1:])


class SwimClient(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self, host = str(), port = int() ):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        
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
        self.MAXPACKETSIZE = 32
        self.HOSTPORT = (self.HOST, self.PORT)
        self.initialize()
        self.stopreceivethread = False
        self.daemon = True
    def initialize(self):
        '''
        initializes connection to server
        '''
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        
        #socket for sending
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
       
        # sets socket to be nonblocking, if data can't immediately be sent or received then an exception is raised
        self.SOCK.setblocking(0)
        
        #Find the server
        self.setpayload("Hello!")
        self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)

        while not self.ISCONNECTED:
            try:
                self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
                data, addr = self.SOCK.recvfrom(32)
                #print data, addr
                if data.strip() == 'hello client':
                    print"I've found the server"
                    self.ISCONNECTED = True 
                time.sleep(1)
            except error:
                continue        
    def send(self):
        if len(self.PAYLOAD)<=self.MAXPACKETSIZE and len(self.PAYLOAD)>0:
            self.SOCK.sendto(self.PAYLOAD,self.HOSTPORT)
            self.SOCK.sendto('done',(self.HOST,self.PORT))
        else:
            self.SOCK.sendto(self.PAYLOAD[:self.MAXPACKETSIZE], self.HOSTPORT)
            self.helpersend(self.PAYLOAD[self.MAXPACKETSIZE:])            
    def helpersend(self,payload):
        '''
        don't call helpersend directly.  
        '''
        if len(payload)<=self.MAXPACKETSIZE and len(payload)>0:
            self.SOCK.sendto(payload,self.HOSTPORT)
            self.SOCK.sendto('done', self.HOSTPORT)
        else:
            self.SOCK.sendto(payload[:self.MAXPACKETSIZE], self.HOSTPORT)
            self.helpersend(payload[self.MAXPACKETSIZE:])
            
    def isconnected(self):
        self.SOCK.sendto("you there?",self.HOSTPORT)
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(5.0)
       
        try: 
            receivedstring = self.SOCK.recv(16)    
            if receivedstring == "yeah bro":
                return True
        except:
            return False
        
    def setpayload(self, payload):
        self.PAYLOAD = payload
        
    def getreceive(self):
        return self.RECEIVE
    
    def receive(self, size = int()):
        self.RECEIVE = ''
        receivedstring = str()
        while 1:
            try:
                receivedstring = self.SOCK.recv(size)
            except error:
                continue
            if receivedstring == 'done':
                break
            else:
                self.RECEIVE = self.RECEIVE + receivedstring  
    def run(self):
        while c.stopreceivethread == False:
            self.receive(self.MAXPACKETSIZE)
            print "RPI says: " + self.RECEIVE
        

if __name__=='__main__':
    #from swim_client import SwimClient
    
    #Command Line helper
    import sys
    try:
        IP,PORT = str(sys.argv[1]),int(sys.argv[2])
    except:
        print "try: python swim_client.py <SERVERIP> <PORT>"
        exit(1)
    ####################
    
    while 1:
        try:
            #setup()    
            c = SwimClient(IP,PORT)
            c.start()
            ############

            #loop()
            while c.ISCONNECTED:
                c.setpayload(raw_input("What: "))
                c.send()
                
               ###Connection Checking doesn't work yet 
               # c.ISCONNECTED = c.isconnected()
                print c.ISCONNECTED
            ##########   
            c.stopreceivethread = True  
            c.SOCK.close()  
        except KeyboardInterrupt:
            print "bye bye"
            exit(0)
           
    



