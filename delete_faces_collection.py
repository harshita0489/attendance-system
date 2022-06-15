
import boto3

if __name__ == "__main__":

    collectionId='testCollection'
    faces=[]
    faces.append("82252eeb-3c42-4f9f-a1e4-e38ea280e473")

    client=boto3.client('rekognition')

    response=client.delete_faces(CollectionId=collectionId,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)