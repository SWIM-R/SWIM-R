

import sys, os


add_to_path = sys.path.append
path_join = os.path.join
mydirname = os.path.dirname(__file__)
if sys.platform is 'linux2' or 'darwin': #if I'm runnning on the rpi or mikes macbook, then go ahead
    add_to_path(path_join(mydirname,'PacketStructure'))
    add_to_path(path_join(mydirname,'EthernetCommunication'))
    add_to_path(path_join(mydirname,'SerialCommunication'))
    add_to_path(path_join(mydirname, 'VideoStreaming'))
else: #otherwise screw you!
    print 'unsupported os!'
    exit(1)





from swim_server import SwimServer
from swim_serial import SwimSerial
#from swim_video import SwimVideo
import time
import platform
from threading import Thread



###############Welcome################
name  = str(sys.argv[0])
print "starting {0}......".format(name)
##################################################


#video = SwimVideo(360,480,5) # height, width, framerate
#def IO():
#    serial = SwimSerial(115200)# Blocking approx 5 seconds when successful
#    ethernet = SwimServer(9999) # blocking, will wait here until it finds the client computer
#    while 1:
#        time.sleep(0.055) 
#
#        try:
#            ethernet.ARDUINOCONNECTION = serial.ISCONNECTED #So the ethernet has some idea about the state of the serial connection
#            if serial.ISCONNECTED:
#                if serial.NEWMESSAGE: # If there is a new message from the Arduino 
#                    if ethernet.ISCONNECTED:
#                        print serial.getreceive()
#                        ethernet.setpayload(serial.getreceive())
#                        ethernet.send()
#                else: #otherwise just ping
#                    ethernet.setpayload({'PING': 0 })
#                    ethernet.send()
#            if serial.ISCONNECTED is False: #ping the error message
#                print "Arduino Broke"
#                ethernet.ARDUINOCONNECTION = False
#                ethernet.setpayload({'PING': 0 })
#                ethernet.send()
#                serial.cleanup()
#                serial = SwimSerial(115200)# Blocking approx 5 seconds when successful  
#           
#            serial.ETHERNETCONNECTION = ethernet.ISCONNECTED #So the serial has some idea about the state of the ethernet connection
#            if ethernet.ISCONNECTED:
#                if ethernet.NEWMESSAGE: #if there is a new message from the Computer
#                    if serial.ISCONNECTED:
#                        serial.setpayload(ethernet.getreceive())
#                        print "down " + ethernet.getreceive()
#                        serial.write()
#                else: #just send the old packet
#                    serial.write()
#    #            if video.frame.new:
#    #                ethernet.setpayload(str(video.get_frame()))
#    #                ethernet.send()
#            if ethernet.ISCONNECTED is False:                
#                print 'ethernet broke'  
#                serial.ETHERNETCONNECTION = False
#                serial.PAYLOAD = [8,1,0,127,127,127,127,127,127]
#                serial.write()
#                ethernet.cleanup()
#                ethernet = SwimServer(9999) # blocking, will wait here until it finds the client computer
#                
#        except KeyboardInterrupt:
#            print "bye bye"
#            exit(0)
#        except Exception as e:
#            print e     
#
#TheThread = Thread(target = IO, args = ())
#TheThread.setDaemon(True)
#TheThread.start()
#while True:
#    if not TheThread.isAlive():
#        time.sleep(1.0)
#        TheThread  = Thread(target = IO, args = ())
#        TheThread.setDaemon(True)
#        TheThread.start()

serial = SwimSerial(115200)# Blocking approx 5 seconds when successful
ethernet = SwimServer(9999) # blocking, will wait here until it finds the client computer
while 1:
    time.sleep(0.055) 

    try:
        ethernet.ARDUINOCONNECTION = serial.ISCONNECTED #So the ethernet has some idea about the state of the serial connection
        if serial.ISCONNECTED:
            if serial.NEWMESSAGE: # If there is a new message from the Arduino 
                if ethernet.ISCONNECTED:
                    print serial.getreceive()
                    ethernet.setpayload(serial.getreceive())
                    ethernet.send()
            else: #otherwise just ping
                ethernet.setpayload({'PING': 0 })
                ethernet.send()
        if serial.ISCONNECTED is False: #ping the error message
            print "Arduino Broke"
            ethernet.ARDUINOCONNECTION = False
            ethernet.setpayload({'PING': 0 })
            ethernet.send()
            serial.cleanup()
            serial = SwimSerial(115200)# Blocking approx 5 seconds when successful  
       
        serial.ETHERNETCONNECTION = ethernet.ISCONNECTED #So the serial has some idea about the state of the ethernet connection
        if ethernet.ISCONNECTED:
            if ethernet.NEWMESSAGE: #if there is a new message from the Computer
                if serial.ISCONNECTED:
                    serial.setpayload(ethernet.getreceive())
                    print "down " + ethernet.getreceive()
                    serial.write()
            else: #just send the old packet
                serial.write()
#            if video.frame.new:
#                ethernet.setpayload(str(video.get_frame()))
#                ethernet.send()
        if ethernet.ISCONNECTED is False:                
            print 'ethernet broke'  
            serial.ETHERNETCONNECTION = False
            serial.PAYLOAD = [8,1,0,127,127,127,127,127,127]
            serial.write()
            ethernet.cleanup()
            ethernet = SwimServer(9999) # blocking, will wait here until it finds the client computer

    except KeyboardInterrupt:
        print "bye bye"
        exit(0)
    except Exception as e:
        print "something broked"
        if platform.system() == 'Darwin':
            with open('/Users/Mike/Desktop/errorlog.txt','a') as f:
                print e
                f.write(str(e)+'\n')        
        elif platform.system() == 'Linux':
            with open('/home/pi/Desktop/errorlog.txt','a') as f:
                print e
                f.write(str(e)+'\n')   
        else:
            print e     
