
from swim_client import SwimClient

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
        
        
        #cleanup() 
        #Things in this section are called if something goes wrong in loop
        c.stopreceivethread = True  
        c.SOCK.close()  
        ######
    except KeyboardInterrupt:
        print "bye bye"
        exit(0)