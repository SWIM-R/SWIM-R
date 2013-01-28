
from swim_server import SwimServer
while 1:
        
        try:
            #setup()
            c = SwimServer(9999)
            c.start()
            #######
            
            #loop()
            while c.ISCONNECTED:
                c.setpayload(raw_input("What: "))
                c.send()
                #c.ISCONNECTED = c.isconnected()
                print c.ISCONNECTED
            #######
            c.stopreceivethread = True
            c.SOCK.close()
        except KeyboardInterrupt:
            print "bye bye" 
            exit(0)
