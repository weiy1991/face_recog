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
import math

encoding_path = "face_encoding.csv"
testing_path = "testing.csv"

if len(sys.argv)==3:
    encoding_path = sys.argv[1]+".csv"
    testing_path = sys.argv[2]+".csv"
else:
    input("please input the path of encoding and testing!")
    #return 0

# Load a sample picture and learn how to recognize it.
#for windows
#obama_image = face_recognition.load_image_file(".\dataset\\Jason\\1.jpg")

# Load all the samples and the responding name lists
picpath=[]
pic_encoding=[]
facename=[]
with open(encoding_path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for item in reader:
        print(item[0], item[1])
        face_image = face_recognition.load_image_file(item[0])
        face_encoding_image = face_recognition.face_encodings(face_image)
        print(len(face_encoding_image))
        if len(face_encoding_image)==1:
            pic_encoding.append(face_encoding_image[0])
            facename.append(item[1])
            print( item[0]+"encoding successfully!")

            # check the encoding of the image
            locationimg = face_recognition.face_locations(face_image)  # top right bottom left
            print(item[0],locationimg)
            cv2.rectangle(face_image,(locationimg[0][3],locationimg[0][0]),(locationimg[0][1],locationimg[0][2]),(255,0,0),5)
            small_face_image = cv2.resize(face_image, (0, 0), fx=0.25, fy=0.25)
            cv2.imshow(item[0], small_face_image)
            #cv2.waitKey(0)            
        else:
            print( item[0]+"has no encoding!")
    csvFile.close()
print(pic_encoding[0])
#input("control")

#load all the testing images
pic_testing_path=[]
name_testing=[]
with open(testing_path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for item in reader:
        print(item[0], item[1])
        pic_testing_path.append(item[0])
        name_testing.append(item[1])
    csvFile.close()


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

#location_now = None
location_formers = []
name_formers = []
score_face_recog = []

# for single_img_path in pic_testing_path:
#     # Grab a single frame from testing images
#     frame = cv2.imread(single_img_path,1)
#     cv2.waitKey(0)

for single_img_path, single_name in zip(pic_testing_path, name_testing):
    time_start = datetime.now()  #get the start time

    # Grab a single frame from testing images
    frame = cv2.imread(single_img_path,1)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    minvalueglobal = 0.0
    nameglobal = ' '


    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame,3)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        name = "Unknown"
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # See if the face is a match for the known face(s)
            #match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
            #print("match:",match)
            #for p_pic_encoding in pic_encoding:
            #match = face_recognition.compare_faces(pic_encoding, face_encoding, 0.45)
            matcheuli = face_recognition.face_distance(pic_encoding, face_encoding)
            minid = np.argmin(matcheuli)
            minvalue = matcheuli.min()
            minvalueglobal = minvalue
            nameglobal = facename[minid]

            location_now = face_location
            print(location_now)

            name = "Unknown"
            if matcheuli.min() < 0.45:
                name = facename[minid]
            else:
                #cal the location of the center point
                x_now = (location_now[3]*1.0 + location_now[1]*1.0) / 2 
                y_now = (location_now[0]*1.0 + location_now[2]*1.0) / 2

                for location_former, name_former in zip(location_formers, name_formers):
                    x_former = (location_former[3]*1.0 + location_former[1]*1.0) / 2 
                    y_former = (location_former[0]*1.0 + location_former[2]*1.0) / 2
                    distance_now_former = math.sqrt(math.pow((x_now - x_former), 2) + math.pow((y_now - y_former), 2))    
                    print("distance_now_former:", distance_now_former)             
                    if distance_now_former<20:
                        name = name_former

            #print("matcheuli:", matcheuli, type(matcheuli),matcheuli.min(), np.argmin(matcheuli))
            #print("match:",match)
            # for i in range(len(match)):
            #     if match[i]:
            #         name = facename[i]
            #         break
                    
#                if match[0]:
#                    name = "jason"

            face_names.append(name)
            name_formers = face_names
            location_formers = face_locations

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        #calculate the score of the recognition
        if name == single_name:
            score_face_recog.append(1)
        else:
            score_face_recog.append(0)

    # Display the resulting image
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,str(minvalueglobal)+"   "+nameglobal,(50,50), font, 1.0,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time_end = datetime.now()  #get the end time

    time_cost = time_end - time_start
    print("time cost for detection:", (time_cost.microseconds / 1000.0) )

#caculate the score of the recognition
score = 100*(sum(score_face_recog) * 1.0 / len(score_face_recog))
print("final score: %f %" % score)

# Release handle to the webcam
cv2.destroyAllWindows()
