#!/usr/bin/env python
from FaceApiWrapper import FaceApiWrapper
import cv2
import sys
import os
import subprocess

filename = sys.argv[1]
temp_file_path = "./temp_vid_imgs/"
print("***Checking the video: %s***" % filename)
if filename.endswith('.mov') or filename.endswith('.mp4'):
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(temp_file_path + "frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
print("***Video Completed***")

print("***Extracting .wav***")
command = "ffmpeg -i %s -vn -acodec pcm_s16le ./temp_vid_imgs/temp_audio.wav" % filename
subprocess.call(command, shell=True)
print("***Wav Completed***")

#face_api = FaceAPI("cool group bruh", "06a02dcf749e47ae98e737eb5b6cbec1", "eastus2")
#if(sys.argv[2] == 'train'):
#    print("train")
#elif(sys.argv[2] == 'verify'):
#    print("verify")
#elif sys.argv[2] == 'insert_person':
#    print("insert")

print("***Deleting Old Files***")
for the_file in os.listdir(temp_file_path):
    file_path = os.path.join(temp_file_path, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)