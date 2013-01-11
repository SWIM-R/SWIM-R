from swim_client import SwimClient

c = SwimClient('153.106.75.171',9999)

while 1:
    shit = raw_input("what?: ")
    c.setpayload(shit)
    c.send()
    c.receive(64)
    print "RPi says: " + c.getreceive()