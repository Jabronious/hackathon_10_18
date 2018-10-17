import requests
import json
import os

class FaceApiWrapper(object):
    def __init__(self, group_name, key, location):
        # Define General Global Variables
        self.GROUP_NAME = group_name

        # Define Face-API Specific Global Variables
        self.FACE_API_KEY = key
        self.FACE_API_URL = 'https://%s.api.cognitive.microsoft.com/face/v1.0' % (location)
        self.HEADERS = {
            'Ocp-Apim-Subscription-Key': self.FACE_API_KEY,
            'Content-Type': 'application/octet-stream'
        }

        self.PARAMS = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'true',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }


     # 1. Create the Person Group
    def createPersonGroup(self):
        path = self.FACE_API_URL + "/persongroups/" + self.GROUP_NAME
        self.HEADERS['Content-Type'] = "application/json"

        try:
            response = requests.put(path, headers=self.HEADERS, data=json.dumps({"name": self.GROUP_NAME}))
            data = response.json()
            return data
        except Exception as e:
            print(e)


    #  2. Insert People into Person Group
    def insertPersonIntoGroup(self, person_name):
        self.HEADERS['Content-Type'] = "application/json"
        path = self.FACE_API_URL + "/persongroups/" + self.GROUP_NAME +"/persons" 
        body = {
            "name": person_name
        }
        try:
            response = requests.post(path, headers=self.HEADERS, data=json.dumps(body))
            data = response.json()
            return data
        except Exception as e:
            print(e)
        return None


    # 3. Submit Images to Train Face On
    #Obama_ID = "f9a6fb5d-2c81-40c0-9cb0-e9980d62371c"
    def submitPersonImages(self, person_id, image_path):
        # Obtain full URL Path
        path = self.FACE_API_URL + "/persongroups/%s/persons/%s/persistedFaces" % (self.GROUP_NAME, person_id)
    
        for filename in os.listdir(image_path):
            if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                try:
                    img_data = open(image_path + filename, "rb").read()
                    response = requests.post(path, headers=self.HEADERS, data=img_data)
                    faces = response.json()
                    return faces
                except Exception as e:
                    print(e)
            else:
                print("%s is not a supported format" % filename)
        


    # 4. Train Person Group
    def trainPersonGroup(self):
        path = self.FACE_API_URL + "/persongroups/%s/train" % (self.GROUP_NAME)
        try:
            response = requests.post(path, headers=self.HEADERS)
            data = response.json()
            return data
        except Exception as e:
            print(e)
        return
        
    #trainPersonGroup()


    # # 5. Identify Obama
    def detectFace(self, image_data):
        params = ({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'emotion',
        })
    
        path = self.FACE_API_URL + '/detect'
    
        try:
            response = requests.post(path, headers=self.HEADERS, params=params, data=image_data)
            faces = response.json()
            return faces
        except Exception as e:
            print(e)
        return None


    #  Identify person's face
    def identifyPerson(self, face_id):
        body = {
            "personGroupId": self.GROUP_NAME,
            "faceIds": [face_id],
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5
        }
    
        # Obtain full URL Path
        path = self.FACE_API_URL + "/identify"
    
        try:
            response = requests.post(path, headers=self.HEADERS, data=json.dumps(body))
            faces = response.json()
            return faces
        except Exception as e:
            print(e)
        return None


    def getFaceIdentification(self, image):
        image_data = open(image, "rb").read()
        face_detection = self.detectFace(image_data)
        face_identity = self.identifyPerson(face_detection[0]['faceId'])
        return face_detection, face_identity
    
    # Loop through Obama picture directory.
    #img_path = './Obama/'
    #for filename in os.listdir(img_path):
    #    if filename.endswith('.jpg') or filename.endswith('.jpeg'):
    #        print(getFaceIdentification(img_path + filename))




    #image_folder_path = "C:\\hackathon\\voicepassword\\IMG_0909\\IMG_0909_012.jpg"
    #image_data = open(image_path, "rb").read()

