'''
Created on Oct 17, 2012

@author: Mike
'''

MAXPACKETSIZE = 8192
from swim_client import SwimClient
import cv

C = SwimClient(host = '76.235.170.146', port = 9999)

while True:
    C.setpayload('gimme')
    C.send()
    
    C.receive(1024)
    format_string = C.getreceive()
    
    rows,cols,step,size = format_string.split(',')
    
    rows=int(rows)
    cols=int(cols)
    step=int(step)
    size=int(size)
    

    
    C.receive(size)
    image_string = C.getreceive()
    #create a new matrix with the same dimensions as jpeg_mat
    new_mat = cv.CreateMat(rows, cols, cv.CV_8UC1)

    #set the data in new_mat with the string data
    cv.SetData(new_mat, image_string, step)
    
    #decode the matrix into a raw image and display
    frame_2 = cv.DecodeImage(new_mat)
    cv.ShowImage('jpeg', frame_2)

    #wait for a button press, but only for 10 time units.
    #k can be used to quit/change camera/ other stuff by adding more code.
    k = cv.WaitKey(10)
