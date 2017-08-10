# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import face_recognition
import cv2
import csv
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
#for windows
#obama_image = face_recognition.load_image_file(".\dataset\\Jason\\1.jpg")

#for linuxe
obama_image = face_recognition.load_image_file("./dataset/dahang/1.jpg")

obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
print(obama_face_encoding)

# Load all the samples and the responding name lists

log_path = "face_encoding.csv"
picpath=[]
pic_encoding=[]
facename=[]
with open(log_path, 'r') as csvFile:
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
            cv2.rectangle(face_image,(locationimg[0][0],locationimg[0][1]),(locationimg[0][2],locationimg[0][3]),(255,0,0),5)
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

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        name = "Unknown"
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            #match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
            #print("match:",match)
            #for p_pic_encoding in pic_encoding:
            #match = face_recognition.compare_faces(pic_encoding, face_encoding, 0.45)
            matcheuli = face_recognition.face_distance(pic_encoding, face_encoding)
            minid = np.argmin(matcheuli)
            minvalue = matcheuli.min()

            name = "Unknown"
            if matcheuli.min() < 0.4:
                name = facename[minid]
            
            print("matcheuli:", matcheuli, type(matcheuli),matcheuli.min(), np.argmin(matcheuli))
            #print("match:",match)
            # for i in range(len(match)):
            #     if match[i]:
            #         name = facename[i]
            #         break
                    
#                if match[0]:
#                    name = "jason"

            face_names.append(name)

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

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
