'''
Created on Jan 10, 2013

@author: Mike
'''
import socket
import threading
import time
import ast
import subprocess
import smtplib
import string


from socket import error
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
        self.MAXPACKETSIZE = 4095
        self.daemon = True
        self.TIMEOUT = 3.0
        self.stopreceivethread = True
        if PORT == 0:
            PORT = 9999
        
        self.initialize(PORT)
        self.NEWMESSAGE = False
        self.ARDUINOCONNECTION = bool()
        self.WRITE_INSTRUCTIONFORMAT = 'ERROR','ARM','ROLL', 'PITCH','YAW','X','Y','Z' #The format that should be written to the Arduino
        self.READ_DATAFORMAT = 'ERROR', 'ROLL','PITCH','YAW','TEMPERATURE', 'DEPTH', 'BATTERY' # the format that should come from the Arduino
        
        print "starting receive thread"
        self.start()
        
    def initialize(self,PORT):
        '''
        initializes connection to client, if successfully initialized sets ISCONNECTED to be true
        '''
        
        # SOCK_DGRAM is the socket type to use for UDP sockets
        # AF_INET sets it to use UDP protocol
        self.SOCK = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
        # So that the OS doesn't complain
        self.SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #sets socket to be blocking along with a timeout, if can't be sent or received within 5 seconds then the timeout exception is raised
        self.SOCK.setblocking(1)
        self.SOCK.settimeout(self.TIMEOUT)
        
#        MyIP = self.getmyIP()
#        while MyIP == '127.0.1.1':
#            MyIP = self.getmyIP()
        #Listen to all IPs on system, there should just be one..
        listen_addr = ('',PORT)
#        print listen_addr
        #Bind socket to address
        self.SOCK.bind(listen_addr)
        
        print 'Connecting to Client Computer...'

        #find the client computer
        while not self.ISCONNECTED:
            try:
                self.RECEIVE, self.CLIENTIP = self.SOCK.recvfrom(64)
            except: #timeout
                continue
            if self.CLIENTIP is not None:
                self.ISCONNECTED = True
                self.stopreceivethread = False
                self.SOCK.sendto("hello client",self.CLIENTIP)
                #self.SOCK.sendall("hello client",)
                
            
        print "I've found the client"
        self.RECEIVE = ''
        
    def getmyIP(self):

        ipaddr_string = 'ip -4 addr > /home/pi/Desktop/SWIM-R/Mike/SWIMR/current_ip2.txt'
        subprocess.call(ipaddr_string, shell=True)
        
        ip_file = file('current_ip.txt', 'r')
        for line in ip_file:
            if 'eth0:' in line:
                inet_line = ip_file.next()
                _time = time.asctime()
                inet_string = inet_line[9:(inet_line.index('/'))]
                return inet_string
    
    def getreceive(self):
        '''
        getter for whatever has been received from the Computer
        '''
        self.NEWMESSAGE = False
        return self.RECEIVE
       
    

    def setpayload(self,payload = dict()):
        '''
        setter for the payload that is going to be sent to the Computer
        '''
        payload['ERROR'] = self.generateerrorcode()
        self.PAYLOAD = str(payload)

    
    
    
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
            
    def generateerrorcode(self,):
        if self.ARDUINOCONNECTION: #if the Arduino is connected
            return False #there is no error
        else:
            return True # there is an error
        
        
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
        while receivedstring is not 'done':
            try:
                receivedstring = self.SOCK.recv(size)
            except:#timeout
                print "Swim server receive timeout"
                self.ISCONNECTED = False
                self.stopreceivethread = True
                return
            if receivedstring == 'done':
                if temp is not '':
                    break
                else:
                    continue
            elif receivedstring == 'PING':
                self.NEWMESSAGE = False
                continue
            elif receivedstring == 'Hello!':
                print "Swim Server receive Hello!"
                self.ISCONNECTED = False
                self.NEWMESSAGE = False
                self.stopreceivethread = True
                return
            else:
                temp = temp + receivedstring
                continue
        self.RECEIVE = temp
        self.NEWMESSAGE = True
    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        while not self.stopreceivethread:
            self.receive(self.MAXPACKETSIZE)            
    def cleanup(self):
        '''
        stops closes the socket and stops the receive thread
        '''
        self.stopreceivethread = True 
        self.ISCONNECTED = False
        time.sleep(0.01) 
        self.SOCK.close()