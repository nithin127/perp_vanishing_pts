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


def find_intersection(line):
	intersection = []
	intersection_valid = []
	intersection_invalid = []
	# the list would be appended in the following format:
	#	line1, line2, x_intersection, y_intersection, (1==outside the line segment, 2== inside the line segment)
	for i in range(line.shape[0]):
		for j in range(i+1,line.shape[0]):
			##
			#checking if any of the slopes are infinity
			##
			if (line[i][0][2]-line[i][0][0] == 0):
				mi = float("inf")
			else: mi = (line[i][0][3]-line[i][0][1])/(line[i][0][2]-line[i][0][0])
			if (line[j][0][2]-line[j][0][0] == 0):
				mj = float("inf")
			else: mj = (line[j][0][3]-line[j][0][1])/(line[j][0][2]-line[j][0][0])
			##
			# if one or more of the slopes are infinity, then we must do the following:
			##
			if (mi == float("inf")):
				if (mj == float("inf")):
					intersection.append([i,j,float("inf"),float("inf"),1])
					intersection_valid.append([i,j,float("inf"),float("inf"),1])
				else:
					p_x = line[i][0][0]
					p_y = line[j][0][1] + mj*(p_x-line[j][0][0])
					intersection.append([i,j,p_x,p_y,1])
					intersection_valid.append([i,j,p_x,p_y,1])
			elif (mj == float("inf")):
				p_x = line[j][0][0]
				p_y = line[i][0][1] + mi*(p_x-line[i][0][0])
				intersection.append([i,j,p_x,p_y,1])
				intersection_valid.append([i,j,p_x,p_y,1])
			##
			# if none of the slopes are infinity
			##
			elif (mi==mj):
				intersection.append([i,j,float("inf"),float("inf"),1])
				intersection_valid.append([i,j,float("inf"),float("inf"),1])
			else:
				p_x = (line[j][0][1]-line[i][0][1] + mi*line[i][0][0] - mj*line[j][0][0])/(mi-mj)
				p_y = (mi*line[j][0][1]-mj*line[i][0][1]+mi*mj*(line[i][0][0]-line[j][0][0]))/(mi-mj)
				if (in_lineseg(line[i][0],p_x,p_y) or (in_lineseg(line[j][0],p_x,p_y))):
					intersection.append([i,j,p_x,p_y,0])
					intersection_invalid.append([i,j,p_x,p_y,0])
				else: 
					intersection.append([i,j,p_x,p_y,1])
					intersection_valid.append([i,j,p_x,p_y,1])

	return intersection, intersection_valid, intersection_invalid 

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
		return x

def rank_vanishing_points(intersection_valid, line):
	max_len = find_max_length(line)
	vote =[]
	for point in intersection_valid:
		vote_iter = float(0)
		# If the intersection points is at infinity
		if (point[2] == float("inf")):
			pts = line[point[1]][0]
			if (pts[0]-pts[2] ==0):
				m = float("inf")
			else:
				m = (pts[1]-pts[3])/pts[0]-pts[2]
			for seg in line:
				pts_t = seg[0]			
				if (pts[0]-pts[2] ==0):
					m_t = float("inf")
				else:
					m_t = (pts[1]-pts[3])/pts[0]-pts[2]
				length_t = np.sqrt((pts[1]-pts[3])**2+(pts[0]-pts[2])**2)
				vote_iter = vote_iter + vote_value(m,m_t,length_t,max_len)
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
				vote_iter = vote_iter + vote_value(m,m_t,length_t,max_len)
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
	   raise Exception('lines do not intersect')
	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	return x, y

def find_intersection2(line):
	zero_slope = []
	inf_slope=[]
	other_line=[]

	for i in range(line.shape[0]):
		if (line[i][0][3]-line[i][0][1] == 0):
			#print line[i][0] , 'zero_slope'
			zero_slope.append((line[i],i))
			cv2.line(img,(int(line[i][0][0]),int(line[i][0][1])),(int(line[i][0][2]),int(line[i][0][3])),(255,0,0),2)

	for i in range(line.shape[0]):
		if (line[i][0][2]-line[i][0][0] == 0):
			#print line[i][0] , 'inf_slope'
			inf_slope.append((line[i],i))
			cv2.line(img,(int(line[i][0][0]),int(line[i][0][1])),(int(line[i][0][2]),int(line[i][0][3])),(0,0,255),2)

	for i in range(line.shape[0]):
		if not((line[i][0][2]-line[i][0][0] == 0)or(line[i][0][3]-line[i][0][1] == 0)):
			other_line.append((line[i],i))
			#print line[i][0], mi
	
	intersection = []
	intersection_valid = []
	intersection_invalid = []

	for i in range(len(other_line)):
		mi = (other_line[i][0][3]-other_line[i][0][1])/(other_line[i][0][2]-other_line[i][0][0])
		for j in range(i+1,len(other_line)):
			##
			#checking if any of the slopes are infinity
			##
			mj = (other_line[j][0][3]-other_line[j][0][1])/(other_line[j][0][2]-other_line[j][0][0])	
			if (mi==mj):
				intersection.append([i,j,float("inf"),float("inf"),1])
				intersection_valid.append([i,j,float("inf"),float("inf"),1])
			else:
				p_x = (other_line[j][0][1]-other_line[i][0][1] + mi*other_line[i][0][0] - mj*other_line[j][0][0])/(mi-mj)
				p_y = other_line[j][0][1]+ mj*(p_x-other_line[j][0][0])
				if (in_lineseg(other_line[i][0],p_x,p_y) or (in_lineseg(other_line[j][0],p_x,p_y))):
					intersection.append([i,j,p_x,p_y,0])
					intersection_invalid.append([i,j,p_x,p_y,0])
				else: 
					intersection.append([i,j,p_x,p_y,1])
					intersection_valid.append([i,j,p_x,p_y,1])

