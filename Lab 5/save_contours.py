import numpy as np
import cv2
import sys
import os
import digitalio
import board
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
from PIL import Image
import matplotlib.pyplot as plt
from skimage.io import imsave, imshow, imread
from skimage.color import rgb2hsv, hsv2rgb

#Create the display
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi
# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# create button object
buttonA = digitalio.DigitalInOut(board.D23)

img=None
webCam = False
if(len(sys.argv)>1):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      img = cv2.imread("../data/test.jpg")
      print("Using default image.")

while(True):
   if webCam:
      ret, img = cap.read()

   imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
   ret,thresh = cv2.threshold(imgray,127,255,0)

   contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   img_c = cv2.drawContours(img, contours, -1, (0,255,0), 3)
   if not buttonA.value:
       os.system("scrot output")
       img = Image.open('output')
       file = cv2.imread('output')
       green_filtered = (file[:,:,1] > 150) & (file[:,:,0] < 100) & (file[:,:,2] < 110)
       green_new = file.copy()
       green_new[:, :, 0] = green_new[:, :, 0] * green_filtered
       green_new[:, :, 1] = green_new[:, :, 1] * green_filtered
       green_new[:, :, 2] = green_new[:, :, 2] * green_filtered
       cv2.imwrite('test.png', green_new)
   if webCam:
      cv2.imshow('contours( press q to quit.)',img_c)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         cap.release()
         break
   else:
      break

cv2.imwrite('contour_out.jpg',img_c)
cv2.destroyAllWindows()

