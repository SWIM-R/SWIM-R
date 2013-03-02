'''
Created on Oct 16, 2012

@author: Mike
'''
#!/Library Python

import serial
#from serial import SerialException
import glob
import platform
import threading 
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
            self.BAUDRATE = 38400
        else:
            GOOD_BAUD_RATES = [38400,115200,57600,38400,28800,19200,14400,9600,4800,2400,1200,300]
            if baudrate in GOOD_BAUD_RATES:
                self.BAUDRATE = baudrate
            else:
                self.BAUDRATE = 115200
        threading.Thread.__init__(self)
        self.IS_CONNECTED = False
        self.SERIAL = None
        self.platform = platform.system()
        self.READINSTRUCTIONWIDTH = 6
        self.PAYLOAD = str()
        self.RECEIVE = str()
        self.initialize()
        self.daemon = True
        self.NEWMESSAGE = False
        self.WRITE_INSTRUCTIONFORMAT = 'ROLL', 'PITCH','YAW','X','Y','Z'
        self.READ_INSTRUCTIONFORMAT = str()
    def scan(self):
        if(self.platform == 'Darwin'):
            return  glob.iglob('/dev/tty.usb*') 
        else:
            return glob.iglob('/dev/serial/by-id/*')
            
    def getstatus(self):
        return self.IS_CONNECTED
    
    def getpayload(self):
        return self.PAYLOAD
    
    def setpayload(self, message):
        #self.PAYLOAD = message
        
        self.PAYLOAD = self.formatforArduino(message)

        
    def getreceive(self):
        self.NEWMESSAGE = False
        return self.RECEIVE
        
    def initialize(self):
        '''
            (void)   initialize:
             invoked in several locations.  scans for serial devices, when it finds the arduino, connects to it.  
             This function is also invoked in the case of a disconnect
        '''
        if self.IS_CONNECTED is False:
            self.SERIAL = None
            ports = self.scan()

            while self.IS_CONNECTED is False:
              
                try:
                    self.SERIAL = serial.Serial(port=ports , baudrate=self.BAUDRATE)    
                except:
                    try:
                        ports = self.scan()
                        ports = ports.next()
                    except StopIteration:
                        break
                    #__TODO__ 
                if self.SERIAL is not None:
                    self.SERIAL.flushInput()
                    self.SERIAL.flushOutput()
                    self.IS_CONNECTED = True
                
            del ports 
        
    def read(self): #need to add timeout handling
        try:
            self.RECEIVE = str(self.SERIAL.read(self.READINSTRUCTIONWIDTH))
        except:
            self.IS_CONNECTED = False
            return
        self.NEWMESSAGE = True
        
        
    def write(self):
            try:
                for byte in self.PAYLOAD:
                    self.SERIAL.write(unichr(int(byte)).encode('latin_1'))
            except:
                self.IS_CONNECTED = False
    
    def run(self):
        while self.IS_CONNECTED:
            self.read()
    
    def formatforArduino(self,unformatted_message = str()):
        formatted_message = bytearray()
        dict_of_unformatted_message = dict(unformatted_message)
        for field in self.WRITE_INSTRUCTIONFORMAT:
            try:
                formatted_message.append(dict_of_unformatted_message[field]) 
            except KeyError:
                #handle not enough bytes
                print "not 6 bytes"
                continue
        return formatted_message
            
                 
if __name__  == '__main__':
        s = SwimSerial(38400)
        s.start()
        while 1:
            s.setpayload(str({'YAW': 0}))
            s.write()
            
            
                
        
        
        
        
        
        
        
        
        
