import mysql.connector
import cv2
import os
import boto3
from boto.exception import BotoServerError
from os import listdir
from os.path import isfile, join
from datetime import datetime

def recog():
    
    mydb = mysql.connector.connect(
            host="148.66.138.159",
            user = "harshita",
            passwd = "harshita",
            database = "harshita"
            )

    mycursor = mydb.cursor()

    LARGE_FONT= ("Verdana", 18)
    MEDIUM_FONT= ("Verdana", 14)

    now = datetime.now()
    now1 = now.strftime("%Y-%m-%d-%I-%M")
    now2 = now.strftime("%Y-%m-%d")

    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        
    # Start capturing video
    vid_cam = cv2.VideoCapture(0)
    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('//home//pi//Desktop//IBS_Attendance_Project//haarcascade_frontalface_default.xml')
    # Initialize sample face image
    count = 0
    assure_path_exists("//home//pi//Desktop//IBS_Attendance_Project//dataset//")
    # Start looping
    while True:
        # Capture video frame
        check, image_frame = vid_cam.read()
        # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(image_frame, 1.3, 5)
        # Loops for each faces
        for (x,y,w,h) in faces:
            #(x,y,w,h)=cv2.boundingRect(face)
            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (0,255,0), 3)
            # Increment sample face image
            count += 1
            # Save the captured image into the datasets folder
                
            new_img_name = str(now1) +".png"
            cv2.imwrite("//home//pi//Desktop//IBS_Attendance_Project//dataset//User." + new_img_name, gray[y:y+h,x:x+w])
                
            try:
                bucket = 'imgrecognitionx201'
                collectionId = 'IDCollection'
                threshold = 70
                maxFaces = 2
                imageFile = '//home//pi//Desktop//IBS_Attendance_Project//dataset//User.'+ new_img_name
                        
                client = boto3.client('rekognition')
            
                with open(imageFile, 'rb') as image:
                    response = client.search_faces_by_image(CollectionId=collectionId,
                                                            Image={'Bytes': image.read()},
                                                            FaceMatchThreshold = threshold,
                                                            MaxFaces = maxFaces)
            
                
                    faceMatches = response['FaceMatches']
                   
            except client.exceptions.InvalidParameterException as e:
                label = '{}'.format("No Face Found")
                cv2.putText(image_frame, label, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 240, 150), 2)
                #print('Attendance registered as present')
                return None
              
                
            for match in faceMatches:
                print ('FaceId:' + match['Face']['FaceId'])
                print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                if (match['Similarity'])>90:
                    mycursor.execute("SELECT * FROM users where users.face_id = '"+match['Face']['FaceId']+"'")
                    users = mycursor.fetchall()
                    rows_affected = mycursor.rowcount
                    if(rows_affected==1):
                        print(rows_affected)
                        label = '{}'.format(users[0][2])
                        user_id = '{}'.format(users[0][0])
                        cv2.putText(image_frame, label, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                        #print(now2)
                        
                        mycursor.execute("SELECT * FROM attendance where date(createdDate) = '"+now2+"'")
                        att_count = mycursor.fetchall()
                        rows_affected = mycursor.rowcount
                        if(rows_affected==1):
                            cv2.putText(image_frame, "Attendance Already Done", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                        else:
                            mycursor.execute("Insert into attendance (user_id) values ('"+user_id+"')")
                            if(mycursor.rowcount==1):
                                cv2.putText(image_frame, "Attendance Done", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                            else:
                                cv2.putText(image_frame, "Something Wrong", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                                
                        
                        #print (users)
                    else:
                        label = '{}'.format("User Not Registered")
                        cv2.putText(image_frame, label, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                                
                else:
                    label = '{}'.format("User Not Registered")
                    cv2.putText(image_frame, label, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                    #print('Attendance registered as present')
                    
        # Display the video frame, with bounded rectangle on the person's face   
        cv2.imshow('frame', image_frame)
        #key = cv2.waitKey(1)
            
        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(10) & 0xFF == ord('q'):
            #if key==ord('q'):
            break
        # If image taken reach 100, stop taking video
        elif count>=100:
            print("Successfully Captured")
            break
    # Stop video
    vid_cam.release()
    # Close all started windows
    cv2.destroyAllWindows()


