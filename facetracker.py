#!/usr/bin/env python

import cv2, sys, time, os

# Load the BCM V4l2 driver for /dev/video0. This driver has been installed from earlier terminal commands. 
#This is really just to ensure everything is as it should be.
os.system('sudo modprobe bcm2835-v4l2')
# Set the framerate (not sure this does anything! But you can change the number after | -p | to allegedly increase or decrease the framerate).
os.system('v4l2-ctl -p 40')

# Frame Size. Smaller is faster, but less accurate.
# Wide and short is better, since moving your head up and down is harder to do.
# W = 160 and H = 100 are good settings if you are using and earlier Raspberry Pi Version.
FRAME_W = 320
FRAME_H = 200

# Set up the Cascade Classifier for face tracking. This is using the Haar Cascade face recognition method with LBP = Local Binary Patterns.

cascPath = '/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# Start and set up the video capture with our selected frame size. Make sure these values match the same width and height values that you choose at the start.
cap = cv2.VideoCapture(-1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  320);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200);
time.sleep(2)

#Below we are creating an infinite loop, the system will run forever or until we manually tell it to stop (or use the "q" button on our keyboard)
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == False:
        print("Error getting image")
        continue

    # Convert to greyscale for easier+faster+accurate face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist( gray )

    # Do face detection to search for faces from these captures frames
    faces = faceCascade.detectMultiScale(frame, 1.1, 3, 0, (10, 10))
    
    #Below draws the rectangle onto the screen then determines how to move the camera module so that the face can always be in the centre of screen. 

    for (x, y, w, h) in faces:
        # Draw a green rectangle around the face (There is a lot of control to be had here, for example If you want a bigger border change 4 to 8)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

        break
    
    #Orientate the frame so you can see it.
    frame = cv2.resize(frame, (540,300))
    frame = cv2.flip(frame, 1)
   
    # Display the video captured, with rectangles overlayed
    # onto the Pi desktop 
    cv2.imshow('Video', frame)

    #If you type q at any point this will end the loop and thus end the code.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture information and stop everything
video_capture.release()
cv2.destroyAllWindows()
