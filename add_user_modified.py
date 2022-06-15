import boto3
import mysql.connector
from tkinter import *
import cv2 
import time

    
def capture():
    
    webcam = cv2.VideoCapture(0)
    

    while True:

        try:

            check, frame = webcam.read()

            print(check) #prints true as long as the webcam is running

            print(frame) #prints matrix values of each framecd 

            cv2.imshow("Capturing", frame)

            key = cv2.waitKey(1)
            
            
    
            if key == ord('s'):

                global new_name
                
                new_name="harshita"+ str(time.time())+".jpg"

                cv2.imwrite(filename='//home//pi//Desktop//IBS_Attendance_Project//dataset//'+ new_name, img=frame)

                webcam.release()

                img_new = cv2.imread('//home//pi//Desktop//IBS_Attendance_Project//dataset//'+ new_name, cv2.IMREAD_GRAYSCALE)

                img_new = cv2.imshow("Captured Image", img_new)

                cv2.waitKey(1650)

                print("Processing image...")

                img_ = cv2.imread(new_name, cv2.IMREAD_ANYCOLOR)

                print("Image saved!")
                
                S3 = boto3.client('s3')

                mydb = mysql.connector.connect(
                        host="148.66.138.159",
                        user = "harshita",
                        passwd = "harshita",
                        database = "harshita"
                        )

                mycursor = mydb.cursor()

                if __name__ == "__main__":
                    print(2)
                
                    #new_name="harshita"+str(time.time())+".jpg"
                    SOURCE_FILENAME = '//home//pi//Desktop//IBS_Attendance_Project//dataset//'+ new_name
                    BUCKET_NAME = 'imgrecognitionx201'
                    user_name = params
                    # Uploads the given file using a managed uploader, which will split up large
                    # files automatically and upload parts in parallel.
                    z=S3.upload_file(SOURCE_FILENAME, BUCKET_NAME,new_name)
                    bucket='imgrecognitionx201'
                    collectionId='IDCollection'
                    photo = new_name
                
                    client = boto3.client('rekognition')

                    response = client.index_faces(CollectionId=collectionId,
                                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                                ExternalImageId=photo,
                                                MaxFaces=1,
                                                QualityFilter="AUTO",
                                                DetectionAttributes=['ALL'])

                    print ('Results for ' + photo)     
                    print('Faces indexed:')                        
                    for faceRecord in response['FaceRecords']:
                        print(3)
                        print('  Face ID: ' + faceRecord['Face']['FaceId'])
                        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
                     
                        mycursor.execute("insert into users (face_id,name) values ('"+faceRecord['Face']['FaceId']+"','"+user_name+"') ")
                        mydb.commit()
                        print(mycursor.rowcount, "record inserted.")
                     
                    if mycursor.rowcount==1:
                        print("succesfully stored")
                    else:
                        print("something is wrong")

                cv2.destroyAllWindows()

                break

            elif key == ord('q'):

                print("Turning off camera.")

                webcam.release()

                print("Camera off.")

                print("Program ended.")

                cv2.destroyAllWindows()

                break

        

        except(KeyboardInterrupt):

            print("Turning off camera.")

            webcam.release()

            print("Camera off.")

            print("Program ended.")

            cv2.destroyAllWindows()

            break
    
            

def add_user():

    root1 = Tk()
    root1.title("User Name")
    Label(root1, text = "NAME").grid(row = 0, sticky = W)
    Fname = Entry(root1)
    Fname.grid(row = 0, column = 1)
    

    def getInput():
        global params
        params = Fname.get()
        root1.destroy()
       
       
    Button(root1, text = "submit", command = lambda:[getInput(), capture()]).grid(row = 5, sticky = W)
    
    root1.mainloop()
    

    
    



