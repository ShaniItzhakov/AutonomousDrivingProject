# -*- coding: utf-8 -*-
"""Autonomous_driving_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/145FBKfVI6cF8nglno4OeeKmGxzKFPrSE
"""

bagfile_name = '20220609_143137.bag'
number_of_frames = 100

!pip install cvbridge3 
!pip install pyrealsense2 
!pip install bagpy

from google.colab import drive
drive.mount('/drive')

!git clone https://github.com/ultralytics/yolov5  # clone

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov5
!pip install -qr requirements.txt  # install
# %mkdir -m777 currImage

# Commented out IPython magic to ensure Python compatibility.
def remove_txt():
#   %cd /content/yolov5/runs/detect/exp/
#   %rm -r labels
#   %cd ../../../

import torch
# import utils
import argparse
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import math

from google.colab.patches import cv2_imshow # for image display

# init
######################################
# Configure depth and color streams
bagfile_path = '/drive/My Drive/' + bagfile_name
config = rs.config()
rs.config.enable_device_from_file(config, bagfile_path)
config.enable_stream(rs.stream.depth, 640, 480)
config.enable_stream(rs.stream.color, 640, 480)
pipeline = rs.pipeline()
pipeline.start(config)

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov5
try:
#   %rm -r depth_dir
#   %rm -r color_dir
except:
  pass
# %mkdir -m777 depth_dir
# %mkdir -m777 color_dir

from tifffile import imsave
import numpy as np

minmax_arr = []

idx = 0
while idx<number_of_frames:
      frames = pipeline.wait_for_frames()
      color_frame = frames.get_color_frame()
      depth_frame = frames.get_depth_frame()
      x=color_frame.get_data()
      color_image = np.asanyarray(x)
      # depth_image = np.asanyarray(depth_frame.get_data())
      width= depth_frame.get_width()
      height = depth_frame.get_height()

      depth_image = np.zeros(shape=(height, width))
    
      # for i in range(depth_image.shape[0]):
      #    for j in range(depth_image.shape[1]):
      #       depth_image[i, j] = depth_frame.get_distance(j,i)
      depth_image = np.asanyarray([depth_frame.get_distance(j,i) for i in range(height) for j in range(width)]) 
      depth_image = depth_image.reshape((height, width))
      
      max_val = depth_image.max()
      min_val = depth_image.min()

      minmax_arr.append([min_val,max_val])
      norm_depth_image = (depth_image - min_val)/(max_val-min_val)
      cv2.imwrite("/content/yolov5/color_dir/" + str(idx).zfill(5) + ".png", color_image)
      format = '.tiff'
      imsave("/content/yolov5/depth_dir/" + str(idx).zfill(5) + ".tif", norm_depth_image)
      
      if idx % 100 == 0:
        print("in image number: ", idx)
      idx +=1

remove_txt()
!python "/content/yolov5/detect.py" --weights "/drive/My Drive/best.pt" --source "/content/yolov5/color_dir/" --save-txt --exist-ok

import numpy as np

def parse_lines(path, shape) -> np.ndarray:
    lst = []
    H, W = shape
    with open(path) as f:
        Lines = f.readlines()
        for line in Lines:
            _, x, y, w, h = line.split(" ")
            lst.append([int(float(x) * W) - int(float(w) * W) // 2, int(float(y) * H) - int(float(h) * H) // 2,
                        int(float(w) * W), int(float(h) * H)])
    return np.asanyarray(lst)


def get_depth(xywh, im):
    x, y, w, h = xywh
    im = np.round(im, 1)
    bins = np.sort(np.unique(im))
    ind = np.where(bins >= 1)
    if len(ind) != 0:
      ind = ind[0][0]
    else:
      ind = 0

    bins1 = np.round(bins[0:ind])

    bins2 = np.round(bins[ind:])
    bins = np.concatenate((bins1, bins2))
    bins = np.unique(bins)


    hist,nums = np.histogram(im[y:y + h, x:x + w], bins=bins)
    for index, val in enumerate(nums[:-1]):
      if hist[index] > h*w*1/10:
          return val, x + w // 2, y + h // 2
    return None


def make_decision(res_final, center_dot):
  if res_final[0] < 3:
    if res_final[1] < 320 : return "right"
    else: return "left"
  else:
    left = 0
    right = 0
    for x,y in center_dot:
      if x != res_final[1] and y!=res_final[2]:
        if x > res_final[1]: left +=1
        else: right += 1
    if right>left:
      return "right"
    else: return "left"

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/yolov5
try:
#   %rm -r final_images
except:
  pass
# %mkdir -m777 final_images

from IPython.core.display import Math
import cv2
from osgeo import gdal
import matplotlib.pyplot as plt
import math

i = 0
while i<number_of_frames:
  try:
    if i % 100 == 0:
      print("in image number: ", i)
    color_image = cv2.imread("/content/yolov5/color_dir/" + str(i).zfill(5) + ".png")

    dataset = gdal.Open(r"/content/yolov5/depth_dir/" + str(i).zfill(5) + ".tif")
    band1 = dataset.GetRasterBand(1)
    norm_depth_image = band1.ReadAsArray()
    depth_image = (norm_depth_image * (minmax_arr[i][1] - minmax_arr[i][0])) + minmax_arr[i][0]
    # depth_image = depth_image.astype(int)


    img = color_image

    rects = parse_lines("/content/yolov5/runs/detect/exp/labels/" + str(i).zfill(5) + ".txt", depth_image.shape)
    res_final = [math.inf,0,0]
    center_dot = []
    start_point_left = (150, color_image.shape[0])
    end_point_left = (200, 300)
    start_point_right = (color_image.shape[1]-200,300)
    end_point_right = (color_image.shape[1]-150, color_image.shape[0])
    img = cv2.line(img, start_point_left, end_point_left, (255, 0, 0) , 4)
    img = cv2.line(img, start_point_right, end_point_right, (255, 0, 0) , 4)
    for rec in rects:
        res = None
        res = get_depth(rec, depth_image)
        
        if res is not None :
          center_cord =( rec[0] + rec[2] // 2, rec[1] + rec[3] // 2)
          z_depth = res[0]
          if res[0]>=1: z_depth = int(res[0])

          if z_depth > 0.05:
            cv2.putText(img=img, text=str(z_depth)+" m",org=center_cord,
                      fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.6, color=(0, 0, 0), thickness=5)
            cv2.putText(img=img, text=str(z_depth)+" m",org=center_cord,
                      fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.6, color=(255, 255, 255), thickness=2)
          if color_image.shape[1]-175 > rec[0]+rec[2] > 175 or 175 < rec[0] < color_image.shape[1]-175:
              center_dot.append([rec[0]+rec[2]//2, rec[1] + rec[3]//2])
              z, x_center, y_center = res

              if z < res_final[0]:
                  res_final = (z,x_center,y_center)
    if res_final[1] != 0 and res_final[2] != 0:  # There is any relevant data
        center_dot = np.asanyarray(center_dot)

        RISKY_LENGTH = 5
        if 0.05 < res_final[0] < RISKY_LENGTH:
          dir = make_decision(res_final, center_dot)
          dx = 100
          dy = -150

          if res_final[0] < RISKY_LENGTH//2:
            dx = 150
            dy = 0

          if dir == "left": 
            dx *= -1
          img = cv2.arrowedLine(img, (320, 450), (320+dx, 450+dy),(0,0, 255), 10)

    # plt.imshow(img)
    # plt.show()
  
    cv2.imwrite("/content/yolov5/final_images/" + str(i).zfill(5) + ".png", img)
  except FileNotFoundError:
    pass  
  finally:
    i+=1
    pass

import cv2
import os

image_folder = '/content/yolov5/final_images'
video_name = '/content/yolov5/video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 5, (width,height))
for g in range(number_of_frames):
  image  =str(g).zfill(5) + ".png"
  video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

video_path = video_name
video_convert_path =  '/content/yolov5/final_video.mp4'
os.system(f"ffmpeg -i {video_path} -vcodec libx264 {video_convert_path}")

from google.colab import files
files.download(video_convert_path)

