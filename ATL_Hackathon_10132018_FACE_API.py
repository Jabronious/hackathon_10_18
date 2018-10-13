
# coding: utf-8

# 1. Open a Command Prompt and Paste the following command:
# <code>
# net use Z: \\bigdatacatalog.file.core.windows.net\hackathon10132018 /u:AZURE\bigdatacatalog Cgp5/eQ2DS3aAm56CvEt3AsJMMaTsya6HsXBKUfYlE4AxWgUAHN8UqqkM4sQA6nlRKPHfG4wrAMEH9f9c8Phrw==
# </code>
# 2. Copy the "Z:\hackathon" folder into C: drive. You should now have a C:\hackathon folder.
# 3. Add C:\hackathon\ffmpeg-4.0.2-win64-static\bin to your PATH environment variable
#     To extract all frames from MOV file
#         mkdir IMG_0909
#         ffmpeg -i IMG_0909.MOV IMG_0909/IMG_0909_%03d.jpg
#     To extract WAV/PCM audio from MOV file
#           ffmpeg -y -i IMG_0909.mov -vn -acodec pcm_s16le IMG_0909.wav  
# 4. From the Azure Portal (portal.azure.com):
#     a.Create a ATLHACKRG resource group in EAST US 2 region
#     b.Provision the folllowing Cognitive services:
#         - Speaker Recognition API (Name: Speaker-API, Tier: S0, Region: West US, Resource Group: ATLHACKRG)
#         - Face API (Name: Face-API, Tier: S0, Region: East US 2, Resource Group: ATLHACKRG)
#         - Custom Vision (Name: CustomVision-API, Tier: S0, Region: South Central US, Resource Group: ATLHACKRG)
# 5. Create a Custom Vision project from https://customvision.ai and select "ATLHACKRG" directory
# 
# 

# In[1]:


import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "<INSERT_FACE_API_KEY_HERE>"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the westcentralus region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
face_api_url = 'https://eastus2.api.cognitive.microsoft.com/face/v1.0/detect'


# # Read image from local path

# In[ ]:


image_path = "C:\\hackathon\\voicepassword\\IMG_0909\\IMG_0909_012.jpg"
image_data = open(image_path, "rb").read()

headers = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}


response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
faces = response.json()


# # Reading image from remote URL

# In[17]:


# Set image_url to the URL of an image that you want to analyze.
image_url = 'https://www.entrepreneur.com/dbimages/person/h1/20171002193729-Satya-Nadella-web.jpeg'
response = requests.get(image_url)
image_data = response.content

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}
data = {'url': image_url}
response = requests.post(face_api_url, params=params, headers=headers, json=data)
faces = response.json()


# # Inspect the response JSON

# In[18]:


faces


# # Plot the facial landmarks

# In[20]:


# Display the original image and overlay it with the face information.
#image = Image.open(BytesIO(requests.get(image_url).content)) --From URL
image = Image.open(BytesIO(image_data))

plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    fl = face["faceLandmarks"]
    origin = (fr["left"], fr["top"])
    p = patches.Rectangle(
        origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    
    pl = patches.Circle((fl["pupilLeft"]["x"], fl["pupilLeft"]["y"]),radius=3)
    pr = patches.Circle((fl["pupilRight"]["x"], fl["pupilLeft"]["y"]),radius=3)
    ax.axes.add_patch(pl)
    ax.axes.add_patch(pr)

    ml = [fl["mouthLeft"]["x"], fl["mouthLeft"]["y"]]
    ult = [fl["upperLipTop"]["x"], fl["upperLipTop"]["y"]]
    mr = [fl["mouthRight"]["x"], fl["mouthLeft"]["y"]]
    ulb = [fl["upperLipBottom"]["x"], fl["upperLipBottom"]["y"]]
    unt = [fl["underLipTop"]["x"], fl["underLipTop"]["y"]]
    unb = [fl["underLipBottom"]["x"], fl["underLipBottom"]["y"]]
    
    mouth = patches.Polygon([ml,ult,mr,ulb,ml,unt,mr,unb,ml], color='b')
    ax.axes.add_patch(mouth)
    
    plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]),
             fontsize=20, weight="bold", va="bottom")
    _ = plt.axis("off")

