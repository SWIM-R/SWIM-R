'''
Created on Jan 10, 2013

@author: Mike
'''
import socket
import threading

from socket import error
class SwimServer(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self,PORT = int()):
        threading.Thread.__init__(self)
        self.ISCONNECTED = False
        self.RECEIVE = str()
        self.PAYLOAD = str()
        self.MAXPACKETSIZE = 32
        self.daemon = True
        self.stopreceivethread = False
        if PORT is None:
            PORT = 9999
        
        self.initialize(PORT)
        
    def initialize(self,PORT):
        self.SOCK = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #no blocking!
        self.SOCK.setblocking(0)
        
        #Listen to all IPs on system
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
    
    def run(self):
        while self.stopreceivethread == False:
            self.receive(self.MAXPACKETSIZE)
            print "Client says: " + self.RECEIVE
    def isconnected(self):
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(5.0)
        
        try:
            receivedstring = self.SOCK.recv(16)
            if receivedstring == "you there?":
                self.SOCK.sendto("yeah bro", self.CLIENTIP)
                return True
        except:
            return False
                
        

if __name__ == '__main__':
    while 1:
        
        try:
            #setup()
            ethernet = SwimServer(9999)
            ethernet.start()
            #######
            
            #loop()
            while ethernet.ISCONNECTED:
                ethernet.setpayload(raw_input("What: "))
                ethernet.send()
                #ethernet.ISCONNECTED = ethernet.isconnected()
                print ethernet.ISCONNECTED
            #######
            ethernet.stopreceivethread = True
            ethernet.SOCK.close()
        except KeyboardInterrupt:
            print "bye bye" 
            exit(0)


    
