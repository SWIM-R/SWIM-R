#!/usr/bin/python

# video stream server
import SocketServer
import cv, cv2
import sys

def get_strings():
    valid, frame_mat = camcapture.read()     
    if frame_mat is None or valid is False:
        return False,False
    #create an empty raw image 
    frame = cv.CreateImageHeader((frame_mat.shape[1], frame_mat.shape[0]), cv.IPL_DEPTH_8U, 3)
    #fill the empty image with data from frame_mat
    cv.SetData(frame, frame_mat.tostring(), frame_mat.dtype.itemsize * 3 * frame_mat.shape[1])
    #encode the image to reduce the size (SAVE BANDWIDTH!)
    jpeg_mat = cv.EncodeImage(".jpeg", frame)
    #dump the image (matrix) into a string.  This is what will be sent over the network
    image_string = jpeg_mat.tostring()
    #print the length of the image string
#    print len(image_string)
    #print the approximate number of packets required to send image string
#    print str(len(image_string) / 8192)
    #The matrix format will also have to be sent to reconstruct the image
    format_string = '{0}, {1}, {2}, {3}'.format(jpeg_mat.rows, jpeg_mat.cols, jpeg_mat.step, len(image_string) )
    return format_string,image_string

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
        image_format,image_data = get_strings()
        
#        begin = 0
#        end = 8191
#        step = 8192
        socket.sendto(image_format, self.client_address)
        socket.sendto(image_data, self.client_address)
        
        
if __name__ == "__main__":
    print 'main'
    HOST, PORT = '192.168.1.105', 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    
    camcapture = cv2.VideoCapture(0)
    print camcapture.isOpened()
    
    if not camcapture:
        print "Error opening WebCAM"
        sys.exit(1)
    server.serve_forever()
else:
    print 'not main'