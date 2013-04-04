'''
Created on Oct 17, 2012

@author: Mike
'''
import sys
sys.path.append("../EthernetCommunication")
MAXPACKETSIZE = 8192
from swim_client import SwimClient
import cv

try:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
except:
    print "try: python video_stream_client.py <Server IP address> <PORT>"
    exit(1)

broken = False
C = SwimClient(host = HOST, port = PORT)
requestwhat = 'frame'
while True:
    C.setpayload(requestwhat)
    C.send()
    print "requested frame"
    
    C.receive(128)
    format_string = C.getreceive()
    print format_string
    rows,cols,step,size = format_string.split(',')
    
    rows=int(rows)
    cols=int(cols)
    step=int(step)
    size=int(size)
    
    image_string = str()
    while True:
        print broken
        print '1'
        
        C.receive(MAXPACKETSIZE)
        print '2'
        rec_str = C.getreceive()
        print '3'
        if rec_str == 'Done':
            print '4'
            if len(image_string) == size:
                broken = False
                break
            else:
                broken = True
                print 'broken frame'
                break
        print len(rec_str)
        image_string = ''.join([image_string,rec_str])
    
    print len(image_string)   
   
    if not broken:     
            #create a new matrix with the same dimensions as jpeg_mat
        new_mat = cv.CreateMat(rows, cols, cv.CV_8UC1)
        
        #set the data in new_mat with the string data
        cv.SetData(new_mat, image_string, step)
        
        #decode the matrix into a raw image and display
        frame_2 = cv.DecodeImage(new_mat)   #seg fault is here
        print 'here' 
        cv.ShowImage('jpeg', frame_2)
    
        #wait for a button press, but only for 10 time units.
        #k can be used to quit/change camera/ other stuff by adding more code.
    k = cv.WaitKey(2)
    broken = False
