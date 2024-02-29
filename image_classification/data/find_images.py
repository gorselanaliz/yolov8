import argparse
import os
import shutil
import random
import cv2
from os.path import exists
import numpy as np

# Add Parser
parser = argparse.ArgumentParser()

parser.add_argument("--src", type=str, default="train", help="Folder that contain image")
parser.add_argument("--dest", type=str, default="unused_image", help="Folder that contain unused image")

args = parser.parse_args()

def move_image(path_file, dest_folder):
    if(not os.path.isdir(args.dest)):
        os.mkdir(dest_folder)

    try:
        shutil.move(path_file, dest_folder)
        # print("File copied successfully.")

    # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")   

def check_image(source_folder_img, file):
    path_folder = os.path.join(source_folder_img, file)
    is_dir = os.path.isdir(path_folder)

    if(is_dir):
        for folder in os.listdir(path_folder):
            check_image(path_folder, folder)
    else:
        path_file = os.path.join(source_folder_img, file)        

        if ((file.endswith(".jpg")) or (file.endswith(".png"))):    
            separator = file.find(".")
            filename = file[0:separator]              

            source = os.path.join(source_folder_img, file)
                        
            img = cv2.imdecode(np.fromfile(source, np.uint8), cv2.IMREAD_COLOR)

            if(img is None):
                print(path_file)
                move_image(path_file, args.dest)

# Count number of data
source_folder_img = args.src

for file in os.listdir(source_folder_img):
    check_image(source_folder_img, file)
    