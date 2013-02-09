'''
Created on Jan 10, 2013

@author: Mike
'''
import socket
import threading
import time




from socket import error
from socket import timeout
class SwimServer(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self,PORT = int()):
        '''
        Ititializes...everything
        '''
        threading.Thread.__init__(self)
        self.ISCONNECTED = False
        self.RECEIVE = str()
        self.PAYLOAD = str()
        self.MAXPACKETSIZE = 8196
        self.daemon = True
        self.TIMEOUT = 3.0
        self.stopreceivethread = False
        if PORT is None:
            PORT = 9999
        
        self.initialize(PORT)
        self.LASTMESSAGE = str()
        
    def initialize(self,PORT):
        '''
        initializes connection to client, if successfully initialized sets ISCONNECTED to be true
        '''
        
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        #socket for sending
        self.SOCK = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        
        
        # sets socket to be nonblocking, if data can't immediately be sent or received then an exception is raised
        #self.SOCK.setblocking(0)
        
        #sets socket to be blocking along with a 5.0 second timeout, if can't be sent or received within 5 seconds then the timeout exception is raised
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(self.TIMEOUT)
        
        
        #Listen to all IPs on system, there should just be one..
        listen_addr = ("",PORT)
        
        #Bind socket to address
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
                
            
        print "I've found the client"
        self.RECEIVE = ''
    
    def getreceive(self):
        '''
        getter for whatever has been received
        '''
        while self.LASTMESSAGE == self.RECEIVE:
            continue
        return self.RECEIVE
    def getpayload(self):
        '''
        This method is probably useless
        '''
        return self.PAYLOAD
    def setpayload(self,payload = str()):
        '''
        setter for the payload that is going to be sent 
        '''
        self.PAYLOAD = payload
    
    
    
    def send(self):
        '''
        sends whatever is in self.PAYLOAD. calls helpersend if it is large message.  Sends 'done' at the end of a packet
        '''
        if len(self.PAYLOAD) <= 0:
            return
        elif len(self.PAYLOAD)<=self.MAXPACKETSIZE:
            self.SOCK.sendto(self.PAYLOAD,self.CLIENTIP)
            self.SOCK.sendto('done',self.CLIENTIP)
        else:
            self.SOCK.sendto(self.PAYLOAD[:self.MAXPACKETSIZE], self.CLIENTIP)
            self.helpersend(self.PAYLOAD[self.MAXPACKETSIZE:])
            
    def helpersend(self,payload):
        '''
        don't call helpersend directly.  sends 'done' at the end of a packet
        '''
        time.sleep(.001)
        if len(payload)<=self.MAXPACKETSIZE and len(payload)>0:
            self.SOCK.sendto(payload,self.CLIENTIP)
            self.SOCK.sendto('done',self.CLIENTIP)
        else:
            self.SOCK.sendto(payload[:self.MAXPACKETSIZE],self.CLIENTIP)
            self.helpersend(payload[self.MAXPACKETSIZE:])
   
    def receive(self,size = int()):
        '''
        receives a packet until it gets 'done'.  the packet is stored in RECEIVE
        '''
        receivedstring = str()
        temp = str()
        while 1:
            try:
                receivedstring = self.SOCK.recv(size)
            except timeout:
                self.ISCONNECTED = False
                self.stopreceivethread = True
                return
            if receivedstring == 'done':
                break
            if receivedstring == 'Hello!':
                self.setpayload('hello client')
                self.send()
                return
            else:
                temp = temp + receivedstring
            self.LASTMESSAGE = self.RECEIVE
            self.RECEIVE = temp
    
    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        while self.stopreceivethread == False:
            self.receive(self.MAXPACKETSIZE)
            print "Client says: " + self.getreceive()
            
    def cleanup(self):
        '''
        stops closes the socket and stops the receive thread
        '''
        self.stopreceivethread = True 
        time.sleep(0.001) 
        self.SOCK.close()
    def isconnected(self):
        '''
        This doesn't work yet.  It probably wont, dont use it
        
        '''
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(5.0)
        receivedstring = self.SOCK.recv(16)
        if receivedstring == "you there?":
            self.SOCK.sendto("yeah bro", self.CLIENTIP)
            return True
    
        return False
                
        

#if __name__ == '__main__':
#    while 1:
#        
#        try:
#            #setup()
#            ethernet = SwimServer(9999)
#            ethernet.start()
#            #######
#            
#            #loop()
#            while ethernet.ISCONNECTED:
#                ethernet.setpayload(raw_input("What: "))
#                ethernet.send()
#                #ethernet.ISCONNECTED = ethernet.isconnected()
#                print ethernet.ISCONNECTED
#            #######
#            ethernet.stopreceivethread = True
#            ethernet.SOCK.close()
#        except KeyboardInterrupt:
#            print "bye bye" 
#            exit(0)


    
