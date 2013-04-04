import cv, cv2
import sys        

camcapture = cv2.VideoCapture(0)
print camcapture.isOpened()
 
if not camcapture:
        print "Error opening WebCAM"
        sys.exit(1)
 
while True:
    valid, frame_mat = camcapture.read() 
    
    if frame_mat is None or valid is False:
        break
    
    #create an empty raw image 
    frame = cv.CreateImageHeader((frame_mat.shape[1], frame_mat.shape[0]), cv.IPL_DEPTH_8U, 3)
    
    #fill the empty image with data from frame_mat
    cv.SetData(frame, frame_mat.tostring(), frame_mat.dtype.itemsize * 3 * frame_mat.shape[1])
    
    #encode the image to reduce the size (SAVE BANDWIDTH!)
    jpeg_mat = cv.EncodeImage(".jpeg", frame)
    
    #dump the image (matrix) into a string.  This is what will be sent over the network
    image_string = jpeg_mat.tostring()
    
    #print the length of the image string
    print len(image_string)
    
    #print the approximate number of packets required to send image string
    print str(len(image_string) / 8192)
    
    #The matrix format will also have to be sent to reconstruct the image
    format_string = '{0}, {1}, {2}, {3}'.format(jpeg_mat.rows, jpeg_mat.cols, jpeg_mat.step, len(image_string) )
    
    ##################################################
    #Pretend the following is on a different computer#
    ##################################################
    
    #receive format_string from socket
    #receive image_string from socket
    
    rows,cols,step,length = format_string.split(',')
    
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

    #wait for a button press, but only for 10 time units.
    #k can be used to quit/change camera/ other stuff by adding more code.
    k = cv.WaitKey(10)