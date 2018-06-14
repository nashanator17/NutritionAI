import numpy as np
import argparse
import cv2
import os

# Parser for image
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# Read image
image = cv2.imread(args["image"],0)
# Create mask
mask = np.ones(image.shape[:2], dtype="uint8") * 255
# Adaptive threshold
image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
# Binary flip image for erosion and dilation
image = cv2.bitwise_not(image)
# Erode and Dilatee iteratively
for i in range (30):
    
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image,kernel,iterations = 1)
    image = cv2.dilate(image,kernel,iterations = 1)
    
# Deskew the image
coords = np.column_stack(np.where(image > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
	angle = -(90 + angle)
else:
	angle = -angle
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# find all contours, loop through them, and mask the contours that have too small of an area
_, contours, hierarchy = cv2.findContours(rotated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    area = cv2.contourArea(c)
    if area < 50 or w < 8 or h < 8:
        cv2.drawContours(mask, [c], -1, 0, -1)

# bitwise AND with mask to omit unwanted areas
rotated = cv2.bitwise_and(rotated, rotated, mask=mask)

# Binary flip image to be fed into tesseract for ocr
rotated = cv2.bitwise_not(rotated)

# Save resulting image
cv2.imwrite('processed.png',rotated)