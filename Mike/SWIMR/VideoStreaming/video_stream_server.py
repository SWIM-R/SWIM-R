#!/usr/bin/python

# video stream server
import SocketServer
import cv, cv2
import sys
####

def recursive_send(socket, data_string, address):
    if len(data_string)<=8192 and len(data_string)>0:
        socket.sendto(data_string,address)
        socket.sendto('Done', address)
    else:
        socket.sendto(data_string[:8192], address)
        cv.WaitKey(1)
        recursive_send(socket, data_string[8192:], address)
            
def get_frame():
    valid, frame_mat = camcapture.read()     
    if frame_mat is None or valid is False:
        return None, None
    #create an empty raw image 
    frame = cv.CreateImageHeader((frame_mat.shape[1], frame_mat.shape[0]), cv.IPL_DEPTH_8U, 3)
    #fill the empty image with data from frame_mat
    cv.SetData(frame, frame_mat.tostring(), frame_mat.dtype.itemsize * 3 * frame_mat.shape[1])
    #encode the image to reduce the size (SAVE BANDWIDTH!)
    jpeg_mat = cv.EncodeImage(".jpeg", frame)
    #dump the image (matrix) into a string.  This is what will be sent over the network
    image_string = jpeg_mat.tostring()
    #The matrix format will also have to be sent to reconstruct the image
    format_string = '{0}, {1}, {2}, {3}'.format(jpeg_mat.rows, jpeg_mat.cols, jpeg_mat.step, len(image_string))
    return format_string, image_string

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    def handle(self):
        print 'handle'
        data = self.request[0].strip()        
        socket = self.request[1]
        print data
        
        if data == 'frame':
            format_string,image_string = get_frame()
            if format_string is None or image_string is None:
                print "bad frame!!"
                return
            else:
                socket.sendto(format_string, self.client_address)
                print 'sent frame!! of size {0} to {1}'.format(len(image_string), self.client_address)
                recursive_send(socket, image_string, self.client_address)
                
        else:
            print 'skipping...'    
        
if __name__ == "__main__":
    print 'main'
    HOST, PORT = '153.106.113.107', 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    
    camcapture = cv2.VideoCapture(0)
    camcapture.set(cv.CV_CAP_PROP_FRAME_HEIGHT,720)

    camcapture.set(cv.CV_CAP_PROP_FRAME_WIDTH,1280)
    print camcapture.isOpened()
    
    if not camcapture:
        print "Error opening WebCAM"
        sys.exit(1)
    print 'serving...'
    server.serve_forever()
else:
    print 'not main'
