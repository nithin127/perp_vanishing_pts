import numpy as np
import cv2  
import math
import sys 
from PIL import Image
from tempfile import TemporaryFile
import pdb

from functions import find_max_length, find_intersection, rank_vanishing_points
from functions import vote_value, find_intersection2, line_intersection

########################################
#In this section, we detect the edges of the image using Probablistic houghtransform. 
#And draw the edges on the image and write it as houghlines5.jpg
image_dir = 'groundtruth/Images/0000000041.jpg'
img = cv2.imread(image_dir)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,170,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
line = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
t = line.shape[0]
for num in xrange(t):
	x1,y1,x2,y2 = line[num][0]
	cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

#cv2.imwrite('houghlines_'+image_dir[-6:],img)
#just to confirm houghlines detection

line = line.astype(float);
img_hough = img

###### intersection detection ######

#intersection, intersection_valid, intersection_invalid = find_intersection2(line)

#for i in range(len(intersection_valid)):
#	print intersection_valid[i]

###### voting of the detected intersection points ######
#vote = rank_vanishing_points(intersection_valid, line)

'''
for i in range(len(intersection_valid)):
	if (intersection_valid[i][2]!=float("inf")):
		cv2.circle(img,(int(intersection_valid[i][2]),int(intersection_valid[i][2])),3,(100,50,50),-1)
		#print (intersection_valid[i][2],int(intersection_valid[i][2])


cv2.imwrite('intersection_val_'+image_dir[-6:],img)
img = img_hough
'''












