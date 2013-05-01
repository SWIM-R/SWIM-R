'''
Created on Oct 16, 2012

@author: Mike
'''
#!/Library Python

import serial
from serial import SerialException
from serial import SerialTimeoutException
import glob
import platform
import threading 
import ast
import time
class SwimSerial(threading.Thread):
    '''
    class SwimSerial

    provides serial interface to the arduino.
    
    '''
    def __init__(self, baudrate=int()):
        '''
        (void)   constructor:  
            Initializes with given Baud rate.  Default is 115200.  If garbage baud rate is specified, uses default. 
            This is also where the serial port is initialized. 
    '''
       
        
        if baudrate == 0:
            self.BAUDRATE = 115200 #the baurate for the serial connection
        else:
            GOOD_BAUD_RATES = [38400,115200,57600,38400,28800,19200,14400,9600,4800,2400,1200,300]
            if baudrate in GOOD_BAUD_RATES:
                self.BAUDRATE = baudrate
            else:
                self.BAUDRATE = 115200
        threading.Thread.__init__(self) # instance of the thread class
        
        self.ISCONNECTED = False # Is the RPI connected to the Arduino?
        
        self.SERIAL = None #Place Holder for the instance of the serial 
        
        self.platform = platform.system() # what system this is running on 
                
        self.PAYLOAD = [0] #information to be Written to Arduino
        
        self.RECEIVE = dict() #information that has just been read from Arduino
        
        self.daemon = True # So the receive thread is closed when the main thread is closed
        
        self.NEWMESSAGE = False # Is there a new message from the Arduino?
        
        self.READTIMEOUT = 15.0 # Seconds for the read method to read specified number of bytes
       
        self.WRITETIMEOUT = 15.0 # Seconds for the write method to write specified number of bytes, otherwise a timeout exception is thrown
        
        self.ETHERNETCONNECTION = False # Is there an active ethernet connection? 
        
        self.WRITE_INSTRUCTIONFORMAT ='ERROR','ARM' ,'ROLL', 'PITCH','YAW','X','Y','Z' #The format that is written to the Arduino
        ''' #the length of Write instruction format is prepended to the beginning of a formatted message so the Arduino knows how many bytes it will receive'''
     
        self.READ_DATAFORMAT ='ROLL','PITCH','YAW','WATER_TEMPERATURE','CASE_TEMPERATURE','HUMIDITY' , 'DEPTH', 'BATTERY' # the format that should come from the Arduino
        
        self.initialize() 
        '''this blocks'''
        
        
        self.start()

    def scan(self):
        '''
        Returns a glob of all of the USB file descriptors. 
        '''
        if self.platform == 'Darwin':
            return  glob.iglob('/dev/tty.usb*') 
        else:
            return glob.iglob('/dev/serial/by-id/*')
            

    def setpayload(self, message = str()):
        '''
        The bytearray that is about to be written to the Arduino is in PAYLOAD
        '''        
        self.PAYLOAD = self.formatforArduino(message)
        
    def getreceive(self):
        '''
        receive is a dictionary of the information received from the Arduino
        '''
        self.NEWMESSAGE = False
        return self.RECEIVE
        
    def initialize(self):
        '''
        scans for serial devices, when it finds the arduino, connects to it.  Invoked in the constructor
        '''
        print "setting up Arduino..."
        if self.ISCONNECTED is False:
            self.SERIAL = None
            ports = self.scan()

            while self.ISCONNECTED is False:
              
                try:
#                    An optional second argument configures the data, parity, and stop bits. The default is 8 data bits, no parity, one stop bit.
                    self.SERIAL = serial.Serial(port=ports , baudrate=self.BAUDRATE, timeout = self.READTIMEOUT, 
                                                writeTimeout = self.WRITETIMEOUT, bytesize = serial.EIGHTBITS,
                                                parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE,
                                                xonxoff = False, rtscts = False,dsrdtr=False )  
                except: #something didn't work
                    try:
                        ports = self.scan()
                        ports = ports.next()
                    except StopIteration:
                        continue
                    #__TODO__ 
                if self.SERIAL is not None:
                    time.sleep(6.0) # wait for the arduino to be ready
                    self.SERIAL.flushInput()
                    self.SERIAL.flushOutput()
                    self.ISCONNECTED = True
                    print "Arduino Connected"
                
            del ports
    
    def run(self):
        '''
        called when .start() method is called.  multithreading!
        '''
        print "starting receive thread"
        while self.ISCONNECTED:
            time.sleep(0.045)
            self.read() 
        
    def read(self): 
        '''
        read READINSTRUCTIONWIDTH bytes from the port.  A timeout my be triggered
        
        a new data packet is preceeded with $$$
        '''
        try:
            if(self.SERIAL.inWaiting() >= 1):
                temp = list(['A','B','C'])
                header = ''.join(temp)
                try:
                    while True:
                        #temp = str(self.SERIAL.read(1))
                        #if temp == '$':
                        #    break
                        #    
                        #if str(temp[0]) == '$' and str(temp[1]) == '$' and str(temp[2]) == '$':
                        #    break
                        temp.pop(0)
                        temp.append(str(self.SERIAL.read(1)))
#                        print len(temp)
                        header = ''.join(temp) 
                        print header
                        if header == "$$$":
                            print "good header!"
                            break
                            
                except Exception as e:
                    print e
                    self.ISCONNECTED = False
                    return
                if header == '$$$': #then read data packet
                    print 'DID THINGS'
                    for key in self.READ_DATAFORMAT:
                        try:
                            data = str()
                            while True:
                                byte = str(self.SERIAL.read(1))
                                if byte == ',' or byte == '#':
                                    if data is not '':
                                        self.RECEIVE[key] = data
                                        break
                                    else: #it is empty and somthing got messed up
                                        return
                                else:
                                    data = data + byte
                        except: #Timeout 
                            self.ISCONNECTED = False
                            return
                    self.NEWMESSAGE = True
                else:
                    self.ISCONNECTED = True
            else:
                #print 'waiting for data'
                pass
        except: 
            self.ISCONNECTED = False
        
        
    def write(self):
            try:
                for number in self.PAYLOAD:
                    self.SERIAL.write(unichr(number).encode('latin_1')) #So that 0-255 can be encoded into a byte
            except: # timeout
                self.ISCONNECTED = False

    
    def generateerrorcode(self):
        '''
        assess the current state of the ethernet connection and generates an error code to be sent to the Arduino
        
        '''
        if self.ETHERNETCONNECTION: #true for connected, diconnected otherwise
            return False #connected, so no error
        else:
            return True # ethernet not connected, yes error!
    def cleanup(self):
        '''
        If everything gonna die, then cleanup your mess!!
        '''
        try:
            self.SERIAL.flushInput()
            self.SERIAL.flushOutput()
            self.SERIAL.close()
        except:
            pass
    
    def formatforArduino(self,unformatted_message = str()):
        '''
        Takes the flattened dictionary unformatted_message, and properly converts it into a byte array to be written to the Arduino
        '''
        try:
            formatted_message = list() #allocate space for a new list
            
            dict_of_unformatted_message = ast.literal_eval(unformatted_message) #convert the received message into a dictionary
            
            dict_of_unformatted_message['ERROR'] = self.generateerrorcode() #make an entry for the current error code in the dictionary
            
            formatted_message.append(int(self.WRITE_INSTRUCTIONFORMAT.__len__())) # prepend the length of the message to the byte array
            
            for field in self.WRITE_INSTRUCTIONFORMAT:
                try:
                    formatted_message.append(dict_of_unformatted_message[field]) 
                except KeyError: #if something got messed up just send 0 to the arduino, so it doens't iterate through the steps.
                    return list(0)
            return formatted_message
        except Exception as e:#if something got messed up just send 0 to the arduino, so it doens't iterate through the steps.
            print e
            return list(0)
            
                 
if __name__  == '__main__':
        s = SwimSerial(115200)        
        while 1:
            if s.ISCONNECTED: 
                if s.NEWMESSAGE:
                    dictionary = s.getreceive()
                    for key in s.READ_DATAFORMAT:
                        print str(key) + ': ' +dictionary[key]
            else:
                print "broken!"
                s.cleanup()
                s =  SwimSerial(115200)           
        
        
#        dictionary1 = ast.literal_eval("{'ERROR': 0,'YAW':127, 'PITCH':127, 'ROLL': 127 , 'X' : 255 , 'Y' : 127 , 'Z': 127}")
#        dictionary2 = ast.literal_eval("{'ERROR': 0,'YAW':127, 'PITCH':127, 'ROLL': 127 , 'X' : 0 , 'Y' : 127 , 'Z': 127}")
#        counter = 0
#        forward = False
#        while 1:
#            counter += 1
#            if counter > 20:
#                forward = not forward
#                counter = 0
#            if forward:
#                dictionary = dictionary1
#            else:
#                dictionary = dictionary2
#            print dictionary1
#            time.sleep(0.5)
#            s.SERIAL.write(unichr(int(len(dictionary.keys()))).encode('latin_1'))
#            for key in s.WRITE_INSTRUCTIONFORMAT:
#                print key, dictionary[key]
#                s.SERIAL.write(unichr(int(dictionary[key])).encode('latin_1')) #So that 0-255 can be encoded into a byte

            
            
                
        
        
        
        
        
        
        
        
        
