#This file contains some of the functions needed for our Computer Vision project on 
#Camera Caliberation through Vanishing points detection

import numpy as np
import cv2  
import math
import sys 
from PIL import Image
from tempfile import TemporaryFile
import pdb


def find_max_length(line):
	#goes through the list of all lines and outputs the length
	#corresponding to the longest line segment
	l = np.shape(line);
	length = [];
	maxlength  = 0 ; 
	for i in range(l[0]):
		mod = math.sqrt((line[i][0][0]-line[i][0][2])**2 +(line[i][0][1]-line[i][0][3])**2);
		length.append(mod);
		if (mod > maxlength):
			maxlength = mod ; 
			i_arg  = i ;
	return maxlength, i_arg;


def in_lineseg(line,x,y):
	#line is an array in the form of [x1,y1,x2,y2] and (x,y) is a point on the line
	# returns true if the point lies on the line segment
	m1 = (y-line[1])/(x-line[0])
	m2 = (y-line[3])/(x-line[2])
	if (m1*m2 >0):
		return False
	else: return True

def vote_value(m1,m2,length_t,max_len):
	#voting strategy to find most likely vanishing point
	w_1 = 0.10; 
	w_2 = 0.99;
	t = 10.0
	if (m1*m2 == -1):
		th = float("inf")
		return 0.0
	else:
		th = abs(math.degrees(math.atan((m1-m2)/(1+m1*m2))))
		x = w_1*(1-th/t) + w_2*(length_t/max_len[0])
		if (x== float("inf"))or(not(x>3) and not(x<3)):
			return 0.0
		elif (x<=0):
			return 0.0
		else:	
			return x

def vote_vanishing_points(intersection_valid, line):
	max_len = find_max_length(line)
	vote =[]
	for point in intersection_valid:
		vote_iter = float(0)
		count = 0
		# If the intersection points is at infinity
		if (point[2] == float("inf")):
			pts = line[point[1]][0]
			if (pts[0]-pts[2] ==0):
				m = float("inf")
			else:
				m = (pts[1]-pts[3])/(pts[0]-pts[2])
			for seg in line:
				pts_t = seg[0]			
				if (pts[0]-pts[2] ==0):
					m_t = float("inf")
				else:
					m_t = (pts[1]-pts[3])/(pts[0]-pts[2])
				length_t = np.sqrt((pts[1]-pts[3])**2+(pts[0]-pts[2])**2)
				vx = vote_value(m,m_t,length_t,max_len)
				if (vx>0):
					count = count + 1
				vote_iter = vote_iter + vx
			# If the intersection points is not at infinity
		else:
			v_x = point[2]
			v_y = point[3]
			for seg in line:
				pts = seg[0]			
				if (pts[0]-pts[2] ==0):
					m_t = float("inf")
				else:
					m_t = (pts[1]-pts[3])/pts[0]-pts[2]
				length_t = np.sqrt((pts[1]-pts[3])**2+(pts[0]-pts[2])**2)
				m = (0.5*(pts[1]+pts[3])-v_y)/(0.5*(pts[0]-pts[2])-v_x)
				vx = vote_value(m,m_t,length_t,max_len)
				if (vx>0):
					count = count + 1
				vote_iter = vote_iter + vx
		if (count >0):				
			vote_iter = vote_iter/count
		vote.append(vote_iter)
	return vote

def line_intersection(line1, line2):
	pro = line1
	con = line2
	line1 = [pro[0:2],pro[2:4]]
	line2 = [con[0:2],con[2:4]]
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here
	def det(a, b):
	    return a[0] * b[1] - a[1] * b[0]
	div = det(xdiff, ydiff)
	if div == 0:
	   return float("inf"), float("inf")
	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	return x, y

def print_lines(line,img):
	t = line.shape[0]
	for num in range(t):
		x1,y1,x2,y2 = line[num][0]
		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
	return img

def find_intersections(line):
	zero_slope = []
	inf_slope=[]
	other_line=[]
	image_dir = 'groundtruth/Images/0000000041.jpg'

	for i in range(line.shape[0]):
		if (line[i][0][3]-line[i][0][1] == 0):	
			zero_slope.append((line[i],i))
			
	for i in range(line.shape[0]):
		if (line[i][0][2]-line[i][0][0] == 0):		
			inf_slope.append((line[i],i))
			
	for i in range(line.shape[0]):
		if not((line[i][0][2]-line[i][0][0] == 0)or(line[i][0][3]-line[i][0][1] == 0)):
			other_line.append((line[i],i))		

	intersection = []
	intersection_valid = []
	intersection_invalid = []
	# the list would be appended in the following format:
	# [line1, line2, x_intersection, y_intersection]
		
	for i in range(len(other_line)):
		for j in range(i+1,len(other_line)):
			#checking if the lines intersect at all	
			#finding the points of intersection
			p_x,p_y = line_intersection(other_line[j][0][0],other_line[i][0][0])
			if (p_x == float("inf")):
				intersection.append([other_line[i][1],other_line[j][1],float("inf"),float("inf")])
				intersection_valid.append([other_line[i][1],other_line[j][1],float("inf"),float("inf")])
			else:
				if (in_lineseg(other_line[i][0][0],p_x,p_y) or in_lineseg(other_line[j][0][0],p_x,p_y)):
					intersection.append([other_line[i][1],other_line[j][1],p_x,p_y])
					intersection_invalid.append([other_line[i][1],other_line[j][1],p_x,p_y])
				else: 
					intersection.append([other_line[i][1],other_line[j][1],p_x,p_y])
					intersection_valid.append([other_line[i][1],other_line[j][1],p_x,p_y])

	if (len(inf_slope) >1):
		intersection.append([zero_slope[0][1],zero_slope[1][1],float("inf"),float("inf")])
		intersection_valid.append([zero_slope[0][1],zero_slope[1][1],float("inf"),float("inf")])

	if (len(zero_slope) >1):
		intersection.append([inf_slope[0][1],zero_slope[1][1],float("inf"),float("inf")])
		intersection_valid.append([inf_slope[0][1],inf_slope[1][1],float("inf"),float("inf")])

	return intersection, intersection_valid, intersection_invalid 		

