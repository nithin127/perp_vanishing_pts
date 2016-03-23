import numpy as np
import cv2  
import math
import sys 
from PIL import Image
from tempfile import TemporaryFile
import pdb

from functions import find_max_length, find_intersections, vote_vanishing_points
from functions import vote_value, line_intersection, in_lineseg, print_lines

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

#img = print_lines(line,img)
#cv2.imwrite('houghlines_'+image_dir[-6:],img)
#just to confirm houghlines detection

line = line.astype(float);
img_hough = img

###### intersection detection ######

intersection, intersection_valid, intersection_invalid = find_intersections(line)

###### voting of the detected intersection points ######

vote = vote_vanishing_points(intersection_valid, line)
rank = np.argsort(vote)

for i in range(len(intersection_valid)):	
		if not(intersection_valid[rank[i]][2]== float("inf")):
			img = cv2.imread(image_dir)
			cv2.circle(img,(int(intersection_valid[rank[i]][2]),int(intersection_valid[rank[i]][3])),10,(255,0,0),-1)
			cv2.imwrite('vote'+str(i)+image_dir[-6:],img)