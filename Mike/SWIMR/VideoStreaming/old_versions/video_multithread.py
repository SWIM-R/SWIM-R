import cv, cv2
import sys        
import threading
    
def get_frame(): 
    global camcapture
    if not camcapture:
            print "Error opening WebCAM"
            sys.exit(1)

    while True:
        valid,frame_mat = camcapture.read()
        if frame_mat is None or valid is False:
            break
        
        
        
        #create an empty raw image 
        frame = cv.CreateImageHeader((frame_mat.shape[1], frame_mat.shape[0]), cv.IPL_DEPTH_8U, 3)
        
        #fill the empty image with data from frame_mat
        cv.SetData(frame, frame_mat.tostring(), frame_mat.dtype.itemsize * 3 * frame_mat.shape[1])
        
        #encode the image to reduce the size (SAVE BANDWIDTH!)
        jpeg_mat = cv.EncodeImage(".jpeg", frame)
        
        frame_request.wait()
        #dump the image (matrix) into a string.  This is what will be sent over the network

        image_string = jpeg_mat.tostring()
        format_string = '{0}, {1}, {2}'.format(jpeg_mat.rows, jpeg_mat.cols, jpeg_mat.step)
        
        frame_request.clear()
        frame_ready.set()
        
        k = cv.WaitKey(10)

def display_frame():
    while True:
#        global jpeg_frame
        frame_ready.wait()
        global format_string
        global image_string
        frame_ready.clear()
        frame_request.set()
#        frame_2 = cv.DecodeImage(jpeg_frame)
        rows,cols,step = format_string.split(',')
        
        rows=int(rows)
        cols=int(cols)
        step=int(step)
        
        #create a new matrix with the same dimensions as jpeg_mat
        new_mat = cv.CreateMat(rows, cols, cv.CV_8UC1)
    
        #set the data in new_mat with the string data
        cv.SetData(new_mat, image_string, step)
        
        #decode the matrix into a raw image and display
        frame_2 = cv.DecodeImage(new_mat)
        cv.ShowImage('jpeg', frame_2)


        
    
    
if __name__=='__main__':
    camcapture = cv2.VideoCapture(0)
    format_string = str()
    image_string = str()
    
    frame_ready = threading.Event()
    frame_request = threading.Event()
    
    frame_request.set()
    
    frame_grabber = threading.Thread(group=None, target=get_frame, 
                                     name='frame_grabber', args=(), kwargs={})
    
    frame_displayer = threading.Thread(group=None, target=display_frame, 
                                       name='frame_displayer', args=(), kwargs={})
    frame_grabber.start()
    frame_displayer.start()
    
    