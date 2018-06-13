import numpy as np
import argparse
import cv2
import os

# Parser for image
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# read image
image = cv2.imread(args["image"],0)
image = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
# denoise image by closing then opening the image
kernel = np.ones((2,2),np.uint8)
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
# binary flip the image for deskewing
thresh = cv2.bitwise_not(image)
# deskew
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
	angle = -(90 + angle)
else:
	angle = -angle
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
# write image
cv2.imwrite('processed.png',rotated)
# show image
#cv2.imshow("image",rotated)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
