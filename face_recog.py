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

#socket && json
import socket               
import simplejson 

#############TCP socket client#############
host = 'localhost'
port = 8083
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护
client.connect((host, port))
######################################

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
cv2.namedWindow("face_recognition", flags=0);
cv2.setWindowProperty("face_recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);  

# Load a sample picture and learn how to recognize it.
#for windows
#obama_image = face_recognition.load_image_file(".\dataset\\Jason\\1.jpg")

#for linuxe
# obama_image = face_recognition.load_image_file("./dataset/dahang/1.jpg")

# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
# print(obama_face_encoding)

# Load all the samples and the responding name lists

log_path = "face_encoding_id.csv"
picpath=[]
pic_encoding=[]
facename=[]
face_id = []
with open(log_path, 'r') as csvFile:
    reader = csv.reader(csvFile)
    for item in reader:
        print(item[0], item[1], item[2])
        face_image = face_recognition.load_image_file(item[0])
        face_encoding_image = face_recognition.face_encodings(face_image)
        print(len(face_encoding_image))
        if len(face_encoding_image)==1:
            pic_encoding.append(face_encoding_image[0])
            facename.append(item[1])
            face_id.append(item[2])
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

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# time check for socket 
socket_time_former = datetime.now()
socket_time_now = datetime.now()
socket_time_count = 0.0
socket_name = ''
socket_ID = -1

#location_now = None
location_formers = []
name_formers = []

frame_count = 0

while True:

    time_start = datetime.now()  #get the start time

    # count increase
    frame_count+=1

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

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
            #print(location_now)

            name = "Unknown"
            if matcheuli.min() < 0.40:
                name = facename[minid]
            else:
                #cal the location of the center point
                #cal the location of the center point
                    x_now = (location_now[3]*1.0 + location_now[1]*1.0) / 2 
                    y_now = (location_now[0]*1.0 + location_now[2]*1.0) / 2

                    distance_now_formers = []
                    print("name_formers:",name_formers)
                    for location_former, name_former in zip(location_formers, name_formers):
                        x_former = (location_former[3]*1.0 + location_former[1]*1.0) / 2 
                        y_former = (location_former[0]*1.0 + location_former[2]*1.0) / 2
                        distance_now_former = math.sqrt(math.pow((x_now - x_former), 2) + math.pow((y_now - y_former), 2))    
                        distance_now_formers.append(distance_now_former)
                        #print("distance_now_former:", distance_now_former, name_former)
                        # if distance_now_former<20:
                        #     name = name_former
                    #check the distance
                    if len(distance_now_formers)>0:
                        min_distance = min(distance_now_formers)
                        id_distance = -1
                        for i in range(len(distance_now_formers)):
                            if distance_now_formers[i]==min_distance:
                                id_distance = i
                        if min_distance<20 :
                            print("min_distance:", min_distance, "id:", id_distance, name_formers[id_distance] )
                            name = name_formers[id_distance]
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

        #get the name of the socket
        socket_name = name

        # log the image that recognition
        cv2.imwrite("./log/"+str(frame_count)+".jpg", frame)

    # Display the resulting image
    cv2.imshow('face_recognition', frame)

    
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time_end = datetime.now()  #get the end time

    time_cost = time_end - time_start
    print("time cost for detection:", (time_cost.microseconds / 1000.0) )

    ################TCP socket client send################
    #check the time if it is exceed 1 second
    socket_time_now = datetime.now()  #get the end time
    check_socket = (socket_time_now - socket_time_former).microseconds/1000000.0
    socket_time_count +=check_socket
    print("check_socket:",socket_time_count)

    if socket_time_count > 2.0 and socket_name!='Unknown' :
        socket_time_count = 0.0
        socket_time_former = socket_time_now
            
        #get the ID of the face_name
        for i in range(len(facename)):
            if socket_name==facename[i]:
                socket_ID = face_id[i]
                break

        #merge the data to json format
        dic = {"name": socket_name, "ID": socket_ID}  
        st = simplejson.dumps(dic)  
        #print('after dumps ',type(st))  

        #send the data
        client.send(st.encode())
        #print('send data:',st.encode())
        ###############################################

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
