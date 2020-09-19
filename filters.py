from scipy import ndimage
import cv2
import sys
import logging as log
import datetime as dt
from time import sleep
import numpy as np
import os
import subprocess

#cascPath = "haarcascade_frontalface_default.xml"  # for face detection

#if not os.path.exists(cascPath):
    #subprocess.call(['./download_filters.sh'])
#else:
    #print('Filters already exist!')

def nothing(x):
    pass

faceCascade = cv2.CascadeClassifier(r"F:\\data imp\\coding\\github\\my repo\\Dlib Snapchat filters\\haarcascade_frontalface_default.xml")
log.basicConfig(filename='webcam.log',level=log.INFO)

cv2.namedWindow("Video")
cv2.createTrackbar("y axis", "Video", 280, 500, nothing)##creating trackbar scale on output window
cv2.createTrackbar("x axis", "Video", 180, 400, nothing)
video_capture = cv2.VideoCapture(r"F:\\data imp\\coding\\github\\my repo\\Dlib Snapchat filters\\3.mp4")


anterior = 0
mst = cv2.imread('moustache.png')
hat = cv2.imread('cowboy_hat.png')
dog = cv2.imread('dog_filter.png')


def put_moustache(mst,fc,x,y,w,h):
    
    face_width = w
    face_height = h

    mst_width = int(face_width*0.4166666)+1
    mst_height = int(face_height*0.142857)+1

    mst = cv2.resize(mst,(mst_width,mst_height))

    for i in range(int(0.62857142857*face_height),int(0.62857142857*face_height)+mst_height):
        for j in range(int(0.29166666666*face_width),int(0.29166666666*face_width)+mst_width):
            for k in range(3):
                if mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k] <235:
                    fc[y+i][x+j][k] = mst[i-int(0.62857142857*face_height)][j-int(0.29166666666*face_width)][k]
    return fc

def put_hat(hat,fc,x,y,w,h):
    
    face_width = w
    face_height = h
    
    hat_width = face_width+1
    hat_height = int(0.35*face_height)+1
    
    hat = cv2.resize(hat,(hat_width,hat_height))
    
    for i in range(hat_height):
        for j in range(hat_width):
            for k in range(3):
                if hat[i][j][k]<235:
                    fc[y+i-int(0.25*face_height)][x+j][k] = hat[i][j][k]
    return fc

def put_dog_filter(dog,fc,x,y,w,h):
    face_width = w
    face_height = h
    factor = cv2.getTrackbarPos("y axis", "Video")##x=0.375
    factor=factor/1000#0.248
    factor2 = cv2.getTrackbarPos("x axis", "Video")##x=0.375
    factor2=factor2/1000#0.320
    dog = cv2.resize(dog,(int(face_width*1.5),int(face_height*1.75)))
    try:
        for i in range(int(face_height*1.75)):
            for j in range(int(face_width*1.5)):
                for k in range(3):
                    if dog[i][j][k]<235:
                        fc[y+i-int(0.248*h)-1][x+j-int(0.320*w)][k] = dog[i][j][k]###if u want see correct factors then replace this float values with factor and factor2
        return fc
    except:
        pass
    
    
ch = 0
print("Select Filter:1.) Hat 2.) Moustache 3.) Hat and Moustache 4.) Dog Filter")
ch = int(input())
    
    
while True:
    #if not video_capture.isOpened():
        #print('Unable to load camera.')
        #sleep(5)
        #pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = ndimage.rotate(frame, 270)
    frame = cv2.resize(frame, (400, 500))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (400, 500))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
        ,minSize=(40, 40)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.putText(frame,"Person Detected",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        
        if ch==2:
            frame = put_moustache(mst,frame,x,y,w,h)
        elif ch==1:
            frame = put_hat(hat,frame,x,y,w,h)
        elif ch==3:
            frame = put_moustache(mst,frame,x,y,w,h)
            frame = put_hat(hat,frame,x,y,w,h)
        else:
            frame = put_dog_filter(dog,frame,x,y,w,h)

            
          
    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))


    # Display the resulting frame
    out.write(frame)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
out.release()
cv2.destroyAllWindows()

