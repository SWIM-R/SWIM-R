## python socket chat example
## author: Ankur Shrivastava
## licence: GPL v3 

#server
import socket
import threading
import time

SIZE = 4


#instantiate a new TCP/IP socket instance
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#bind to a specific IP address for this computer
soc.bind(('169.254.182.206',5432))

#listen for connections made to the socket with up to 5 backlogged connections
soc.listen(5)

class CThread(threading.Thread):

#constructor, c is the receiving socket instance
    def __init__(self,c):
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt=False
#receives the SIZE of the packet from the connection, reply with OK then receive the message itself.  
    def mrecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        msg = self.conn.recv(int(data))
        return msg
#part of the Thread class.  CThread.start() calls CThread.run()
    def run(self):
        while not self.stopIt:
            msg = self.mrecv()
            print 'recieved->  ',msg

#Takes in two socket objects.  Based on received string, sets one socket to receive and the other to send data
def setConn(con1,con2):
    dict={}
    state = con1.recv(9)
    con2.recv(9)
    if state =='WILL RECV':
        dict['send'] = con1 # server will send data to reciever
        dict['recv'] = con2
    else:
        dict['recv'] = con1 # server will recieve data from sender
        dict['send'] = con2
    return dict

def msend(conn,msg):
    if len(msg)<=999 and len(msg)>0:
        conn.send(str(len(msg)))
        if conn.recv(2) == 'OK':
            conn.send(msg)
    else:
        conn.send(str(999))
        if conn.recv(2) == 'OK':
            conn.send(msg[:999])
            msend(conn,msg[1000:]) # calling recursive


#Accept a connection. The socket must be bound to an address and listening for connections. 
#The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection,
# and address is the address bound to the socket on the other end of the connection.
(c1,a1) = soc.accept()
(c2,a2) = soc.accept()

#See above for setConn function definition
dict = setConn(c1,c2)

#'recv' references the receiving socket.  Both the sending and receiving socket are in the dictionary.
#CThread is a class defined above
thr = CThread(dict['recv'])

#start inherits from the thread class,  This thread handles the receiving of messages
thr.start()
try:
    while 1:
        #always send the raw input to the socket responsible for sending
        msend(dict['send'],raw_input())
except:
    print 'closing'
thr.stopIt=True
msend(dict['send'],'bye!!!')# for stoping the thread
thr.conn.close()
soc.close()
