# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import face_recognition
import cv2
import csv
import numpy as np
from datetime import datetime
import os,sys

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
frame_count = 0

#get the name of the person
#print(sys.argv[:])
name_person = sys.argv[1]
#print(name_person)
#create the new folder path
img_person_path = "./dataset/"+name_person
if not os.path.isdir(img_person_path):
    os.mkdir(img_person_path) 

while True:

    time_start = datetime.now()  #get the start time

    # Grab a single frame of video
    ret, frame = video_capture.read()
    copyframe = frame.copy()
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        
        locationimg = face_recognition.face_locations(frame)  # top right bottom left  171, 468, 439, 200

        if locationimg:
            copyframe = frame.copy()
            print("detect location:",locationimg)
            cv2.rectangle(frame,(locationimg[0][3],locationimg[0][0]),(locationimg[0][1],locationimg[0][2]),(255,0,0),5)
            
            # record the pic
            if cv2.waitKey(1) & 0xFF == ord('r'):
                cv2.imwrite("new.jpg", copyframe)

        cv2.imshow('Video', frame)

    process_this_frame = not process_this_frame

    #write the frame images
    cv2.imwrite(img_person_path+"/"+str(frame_count)+".jpg", copyframe)
    frame_count+=1

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time_end = datetime.now()  #get the end time

    time_cost = time_end - time_start
    print("time cost for detection:", (time_cost.microseconds / 1000.0) )

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
