#!/usr/bin/python

# video stream server
import cv, cv2
from threading import Thread, Timer
import time
from swim_frame import SwimFrame
####


class SwimVideo(Thread):
    def __init__(self, frame_height, frame_width, frame_rate):
        self.FRAME_RATE = frame_rate
        self.cam_id = 0 # opencv internally indexes the attached cameras
        self.frame = SwimFrame(frame_height,frame_width)
        self.open_cam()
        #TODO check that the camera is opened using self.cam.isOpened()
        #threading things        
        Thread.__init__(self)
        self.stopreceivethread = False
        self.daemon = True
        self.start()
        
    def open_cam(self):
        '''
        initialize the camera. must be called to change the camera id
        '''
        self.cam = cv2.VideoCapture(self.cam_id)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self.frame.HEIGHT)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, self.frame.WIDTH)

    def new_frame(self):
        '''
        get a new frame from the webcam
        '''
        if not self.frame.new:
            valid, matrix = self.cam.read()
            if matrix is None or valid is False:
                pass
                
            #create an empty raw image 
            f_raw = cv.CreateImageHeader((matrix.shape[1], matrix.shape[0]), cv.IPL_DEPTH_8U, 3)
            #fill the empty image with data from frame_mat
            cv.SetData(f_raw, matrix.tostring(), matrix.dtype.itemsize * 3 * matrix.shape[1])
            #encode the image to reduce the size (SAVE BANDWIDTH!)
            f_comp = cv.EncodeImage(".jpeg", f_raw)
            #dump the image (matrix) into a string.  This is what will be sent over the network
            f_string = f_comp.tostring()
            #The matrix format will also have to be sent to reconstruct the image
            data = { 'rows': f_comp.rows,
                     'cols': f_comp.cols,
                     'step': f_comp.step,
                     'len' : len(f_string),
                     'str' : f_string
                     }
                     
            self.set_frame(data)
        
    def get_frame(self):
        '''
        accessor for getting frame data
        '''
        return self.frame.get_frame_data()
        
    def set_frame(self, data = dict()):
        '''
        setter for the frame data
        '''
        #should probably check for bad dicts
        self.frame.set_frame_data(data)
    
    def timeout_handler(self):
        self.new_frame()
        timer = Timer(1/self.FRAME_RATE, self.timeout_handler)
        timer.start()
    
    def run(self):
        '''
        implementation of the inherited run() method from the Thread class.  
        This is a separate thread from the main thread that is always receiving information
        '''
        while not self.stopreceivethread:
            time.sleep(1/self.FRAME_RATE)
            self.new_frame()

