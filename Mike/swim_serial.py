'''
Created on Oct 16, 2012

@author: Mike
'''
#!/Library Python

import serial
#from serial import SerialException
import glob

class SwimSerial:
    '''
    class SwimSerial

    provides serial interface to the arduino.
    CONSTANTS:
        SERIAL_PORT_NAME: Name of serial port on computer, this nead to be changed for your particular computer
            
        BAUDRATE: communication data rate.  can be set, default if 115200 baud
        
        IS_CONNECTED: is True if serial connection has been successfully eastblished
        
        INSTRUCTION_SIZE: number of bytes in one instruction
        
        PAYLOAD: string that holds received data
        
        SERIAL: internal interface to serial connection
    
METHODS:

(void)   constructor:  
            Initializes with given Baud rate.  Default is 115200.  If garbage baud rate is specified, uses default. 
            This is also where the serial port is initialized. If it cannot initialize, it will get stuck unti it is. 
    
(void)   initialize:
             invoked in several locations.  scans for serial devices, when it finds the arduino, connects to it.  
             This function is also invoked in the case of a disconnect
    
(bool)   getstatus:
            returns the connection status
                    
    
(string) getpayload:
            returns the 4byte payload that is written with the write() method
            
(void)  setpayload(string message):
            sets the PAYLOAD variable with to message
            
(string)  getreceive:
        returns the 4byte string that was received with the read() method 
            
    
(void)   read: reads 4 bytes from the stream
    
(void)    write: writes 4 bytes to the stream
    
    
    '''
    def __init__(self, baudrate=int()):
       
        
        if baudrate is "":
            self.BAUDRATE = 115200
        else:
            GOOD_BAUD_RATES = [115200,57600,38400,28800,19200,14400,9600,4800,2400,1200,300]
            if baudrate in GOOD_BAUD_RATES:
                self.BAUDRATE = baudrate
            else:
                self.BAUDRATE = 115200
        self.IS_CONNECTED = False
        self.SERIAL = None
        
        self.INSTRUCTION_SIZE = int(4)
        self.PAYLOAD = ''
        self.RECEIVE = ''
        self.initialize();
        
    def scan(self):
        return  glob.iglob('/dev/tty.usb*') 
        
            
    def getstatus(self):
        return self.IS_CONNECTED
    
    def getpayload(self):
        return self.PAYLOAD
    
    def setpayload(self, message):
        self.PAYLOAD = message
        
    def getreceive(self):
        return self.RECEIVE
        
    def initialize(self):
            

        while self.IS_CONNECTED is False:
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
                if self.SERIAL is not None:
                    self.SERIAL.flushInput()
                    self.SERIAL.flushOutput()
                    self.IS_CONNECTED = True
                
            del ports 
        
    def read(self):
        try:
            self.RECEIVE = self.SERIAL.read(self.INSTRUCTION_SIZE)
        except:
            self.IS_CONNECTED = False
            self.initialize()
    def write(self):
            try:
                self.SERIAL.write(self.PAYLOAD)
            except:
                self.IS_CONNECTED = False
                self.initialize()
        
    
            
        
        
        
        
        
        
        
        
        