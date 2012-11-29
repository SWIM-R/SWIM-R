import cv, cv2
import sys        
import Image
import StringIO

camcapture = cv.CreateCameraCapture(0)
cv.SetCaptureProperty(camcapture,cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cv.SetCaptureProperty(camcapture,cv.CV_CAP_PROP_FRAME_HEIGHT, 480);
 
if not camcapture:
        print "Error opening WebCAM"
        sys.exit(1)
 
while True:
    frame = cv.QueryFrame(camcapture)
    if frame is None:
        break
#    <iplimage(nChannels=3 width=640 height=480 widthStep=1920) >
#   encode the image to minimize bandwidth per frame
    jpeg_frame = cv.EncodeImage(".jpeg", frame)
    
    jpeg_data = jpeg_frame.tostring()
#    new_jpeg = Image.fromstring(mode='L', size=(640,480), data=jpeg_data)
#    new_frame = cv.DecodeImage(new_jpeg)
#    cv.ShowImage('converted', new_frame)
    
#    output = StringIO.StringIO()
#    frame.imwrite(output, format='JPEG')
#    frame_jpeg = output.getvalue()
#    output.close()
    
#    print len(frame_jpeg.tostring())
#    print len(jpeg_data)

#    print len(EncodedImage.tostring())
    frame_2 = cv.DecodeImage(jpeg_frame)
#    new_frame = cv.CreateImageHeader( (320,240) ,cv.IPL_DEPTH_8U, 3)
#    cv.SetData(new_frame, image_data)
    cv.ShowImage('jpeg', frame_2)
#    cv.ShowImage('raw',frame)
#    length of the un-encoded image data was 921600
#    print len(image_data)
    k = cv.WaitKey(10)