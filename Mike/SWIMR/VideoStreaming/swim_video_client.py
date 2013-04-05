#!/usr/bin/python

# video stream server
import cv, cv2
import threading
from swim_frame import SwimFrame
####

class SwimVideoClient(threading.Thread):
    def __init__(self, frame_height, frame_width, frame_rate):
        self.FRAME_RATE = frame_rate
        self.frame = SwimFrame(frame_height,frame_width)
        self.image = None
        
        #threading things
        threading.Thread.__init__(self)
        self.stopreceivethread = False
        self.daemon = True
        self.start()

    def get_frame(self):
        '''
        accessor for frame data
        '''
        return self.frame.get_frame_data()
        
    def set_frame(self, data=dict()):
        '''
        setter for the frame data
        '''
        #should probably check for bad dicts
        self.frame.set_frame_data(data)
        
    def create_image(self):
        if self.frame.new:
            print 'new frame'
            #create a new matrix with the same dimensions as jpeg_mat
            new_mat = cv.CreateMat(self.frame.rows, self.frame.cols, cv.CV_8UC1)
            
            #set the data in new_mat with the string data
            cv.SetData(new_mat, self.frame.string, self.frame.step)

            #decode the matrix into a raw image and display
            self.image = cv.DecodeImage(new_mat)   #seg fault is here
            cv.ShowImage('jpeg', self.image)
            self.frame.new = False
            
        #k can be used to quit/change camera/ other stuff by adding more code.
        k = cv.WaitKey(2)
    
    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        while not self.stopreceivethread:
            self.create_image()  
