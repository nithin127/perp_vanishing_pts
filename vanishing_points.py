import numpy as np
import cv2  
import math
import sys 
import matplotlib.pyplot as plt
from PIL import Image
from tempfile import TemporaryFile
import pdb

img = Image.open('groundtruth/Images/0000000041.jpg')
img = np.asarray(img);
edges = cv2.Canny(img,100,200);

#img = np.asarray(img)
#edges = np.asarray(edges)
#print np.shape(img)

#print im1.dtype; Check points in the code 
#print im1.dtype; #check points in the code
###############################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,170,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines5.jpg',img)
print np.shape(lines[0])#Check point for lines data type 
lines = lines.astype(float);
#####################The part after this is only for testing ##########333
line = lines[0];
l = np.shape(line);
length = [];
maxlength  = 0 ; 
for i in range(l[0]):
	mod = math.sqrt((line[i,0]-line[i,2])**2 +(line[i,1]-line[i,3])**2);
	length.append(mod);
	if (mod > maxlength):
		maxlength = mod ; 
		i_arg  = i ;

print max(length);
print maxlength, i_arg;

#m1 = (line[0,3]-line[0,1])/(line[0,2]-line[0,0]);
#m2 = (line[1,3]-line[1,1])/(line[1,2]-line[1,0]);
#print m1,m2 Another testing point 
#x_intersection =( line[1,1] - line[0,1])/(m1-m2) + x1;
#y_intersection =line[1,1] + m2*(x_intersection - line[1,0]);
#print x_intersection , y_intersection
intersection = [];
intersection_valid = [];
intersection_invalid= [];
for i in range(l[0]):
	for j in range(i+1,l[0]):
		if (((line[j,2]-line[j,0])==0) & ((line[i,2]-line[i,0])==0)):
			intersection.append([i,j,float("inf"),float("inf"),1]);
			intersection_valid.append([i,j,float("inf"),float("inf"),1]);#line1,line2,x_intersection,y_interection,outlier(1(for outlier) or 0(inlier))
		elif ((line[j,2]-line[j,0])==0):
 			m1 = (line[i,3]-line[i,1])/(line[i,2]-line[i,0]);
 			x_intersection = line[j,2];
 			y_intersection = m1*(line[j,2]-line[i,0])+line[i,1];
 			p1 = (x_intersection-line[j,0])*(x_intersection-line[j,2]) + (y_intersection-line[j,1])*(y_intersection-line[j,3]);
 			p2 = (x_intersection-line[i,0])*(x_intersection-line[i,2]) + (y_intersection-line[i,1])*(y_intersection-line[i,3]);
 			if (p1 > 0 and p2 > 0):
 				intersection.append([i,j,x_intersection,y_intersection,1]);
 				intersection_valid.append([i,j,x_intersection,y_intersection,1]);
 			else :
 				intersection.append([i,j,x_intersection,y_intersection,0]);
 				intersection_invalid.append([i,j,x_intersection,y_intersection,0]);

 		elif ((line[i,2]-line[i,0])==0):
			m2 = (line[j,3]-line[j,1])/(line[j,2]-line[j,0]);
			x_intersection = line[i,2];
			y_intersection = m2*(line[i,2]-line[j,0])+line[j,1];
			p1 = (x_intersection-line[j,0])*(x_intersection-line[j,2]) + (y_intersection-line[j,1])*(y_intersection-line[j,3]);
 			p2 = (x_intersection-line[i,0])*(x_intersection-line[i,2]) + (y_intersection-line[i,1])*(y_intersection-line[i,3]);
 			if (p1 > 0 and p2 > 0):
 				intersection.append([i,j,x_intersection,y_intersection,1]);
 				intersection_valid.append([i,j,x_intersection,y_intersection,1]);
 			else :
 				intersection.append([i,j,x_intersection,y_intersection,0]);
 				intersection_invalid.append([i,j,x_intersection,y_intersection,0]);
		else : 
			m2 = (line[j,3]-line[j,1])/(line[j,2]-line[j,0]);
			m1 = (line[i,3]-line[i,1])/(line[i,2]-line[i,0]);
			if (m1 == m2):
				 #print "intersection does not exist"
        		 intersection.append([i,j,float("inf"),float("inf"),1]);
        		 intersection_valid.append([i,j,float("inf"),float("inf"),1]);

			else :
				x_intersection =(( line[j,1] - line[i,1]) +(m1*line[i,0]-m2*line[j,0]))/(m1-m2);
				y_intersection =line[j,1] + m2*(x_intersection - line[j,0]);
				p1 = (x_intersection-line[j,0])*(x_intersection-line[j,2]) + (y_intersection-line[j,1])*(y_intersection-line[j,3]);
 				p2 = (x_intersection-line[i,0])*(x_intersection-line[i,2]) + (y_intersection-line[i,1])*(y_intersection-line[i,3]);
 				if (p1 > 0 and p2 > 0):
 					intersection.append([i,j,x_intersection,y_intersection,1]);
 					intersection_valid.append([i,j,x_intersection,y_intersection,1]);
 				else :
 					intersection.append([i,j,x_intersection,y_intersection,0]);
 					intersection_invalid.append([i,j,x_intersection,y_intersection,0]);

N = np.shape(intersection_valid);
w_1 = 0.10; 
w_2 = 0.99;
d_max = 0 ;
vote_data = np.zeros((N[0],8))
vote_data_valid = [];
vote_data_invalid = [];
for i in range(N[0]):
	I = intersection_valid[i][0];
	J = intersection_valid[i][1];
	x_mid_I =  (line[I,0]+line[I,2])/2;
	y_mid_I =  (line[I,1]+line[I,3])/2;
	if ((line[I,3] == line[I,1]) & (line[J,2] == line[J,0])):
		d_1 = float("inf");
	elif((line[I,3] == line[I,1])):
		slope2 = (line[J,3]-line[J,1])/(line[J,2]-line[J,0]);
		x_int = x_mid_I;
		y_int = line[J,1] + slope2*(x_int-line[J,0]);
		d_1 = math.sqrt((x_mid_I-x_int)**2 + (y_mid_I-y_int)**2);
	elif ((line[J,2] == line[J,0])):
		slope1 =(line[I,0]-line[I,2])/(line[I,3]-line[I,1]);
		x_int = line[J,0];
		y_int = y_mid_I +slope1*(x_int-x_mid_I);
		d_1 = math.sqrt((x_mid_I-x_int)**2 + (y_mid_I-y_int)**2);
	else :
		slope1 =(line[I,0]-line[I,2])/(line[I,3]-line[I,1]);
		slope2 = (line[J,3]-line[J,1])/(line[J,2]-line[J,0]);
		if (slope1 == slope2):
			d_1 = float("inf");
		else :
			x_int = ((y_mid_I - line[J,1])-slope1*x_mid_I +slope2*line[J,0])/(slope2-slope1);
			y_int = y_mid_I +slope1*(x_int-x_mid_I);
			d_1 = math.sqrt((x_mid_I-x_int)**2 + (y_mid_I-y_int)**2); 
	#(y-y_mid)/(x-x_mid) = slope1 ; 
	#y = y_mid +slope1*(x-x_mid)   (i)
	#(y-line[J,1])/(x-line[J,0]) = slope2 ; 
	# y = line[j,1] + slope2*(x-line[j,0])   (ii)
	#y_mid - line[j,1] = (slope2-slope1)*x +slope1*x_mid -slope2*line[j,0]
	#((y_mid - line[j,1])-slope1*x_mid +slope2*line[j,0])/(slope2-slope1)=x
	
	##############################################################
	x_mid_J =  (line[J,0]+line[J,2])/2;
	y_mid_J =  (line[J,1]+line[J,3])/2;
	if ((line[J,3] == line[J,1]) & (line[I,2] == line[I,0])):
		d_2 = float("inf");
	elif((line[J,3] == line[J,1])):
		slope2 =(line[I,3]-line[I,1])/(line[I,2]-line[I,0]);
		x_int = x_mid_J;
		y_int = line[I,1] + slope2*(x_int-line[I,0]);
		d_2 = math.sqrt((x_mid_J-x_int)**2 + (y_mid_J-y_int)**2);
	elif ((line[I,2] == line[I,0])):
		slope1 =(line[J,0]-line[J,2])/(line[J,3]-line[J,1]);
		x_int = line[I,0];
		y_int = y_mid_J +slope1*(x_int-x_mid_J);
		d_2 = math.sqrt((x_mid_J-x_int)**2 + (y_mid_J-y_int)**2);
	else :
		slope2 =(line[I,3]-line[I,1])/(line[I,2]-line[I,0]);
		slope1 = (line[J,0]-line[J,2])/(line[J,3]-line[J,1]);
		if (slope1 == slope2):
			d_2 = float("inf");
		else :
			x_int = ((y_mid_J - line[I,1])-slope1*x_mid_J +slope2*line[I,0])/(slope2-slope1);
			y_int = y_mid_I +slope1*(x_int-x_mid_J);
			d_2 = math.sqrt((x_mid_I-x_int)**2 + (y_mid_I-y_int)**2); 
		
	if ((d_1 ==float("inf")) | (d_2 ==float("inf"))):
		length1 = math.sqrt((line[I,0]-line[I,2])**2 + (line[I,1]-line[I,3])**2);
		length2 = math.sqrt((line[J,0]-line[J,2])**2 + (line[J,1]-line[J,3])**2);
		data = np.asarray([I,J,intersection_valid[i][2],intersection_valid[i][3],d_1,d_2,length1,length2]);
		vote_data = data;
		vote_data_invalid.append(data);
	else : 
		if ((d_max  < d_1) | (d_max < d_2) ):
			d_max = max(d_1,d_2);
		length1 = math.sqrt((line[I,0]-line[I,2])**2 + (line[I,1]-line[I,3])**2);
		length2 = math.sqrt((line[J,0]-line[J,2])**2 + (line[J,1]-line[J,3])**2);
		#print d_1,d_2
		data = np.asarray([I,J,intersection_valid[i][2],intersection_valid[i][3],d_1,d_2,length1,length2]);
		vote_data = data;
		vote_data_valid.append(data);

	#(y-y_mid)/(x-x_mid) = slope1 ; 
	#y = y_mid +slope1*(x-x_mid)   (i)
	#(y-line[J,1])/(x-line[J,0]) = slope2 ; 
	# y = line[j,1] + slope2*(x-line[j,0])   (ii)
	#y_mid - line[j,1] = (slope2-slope1)*x +slope1*x_mid -slope2*line[j,0]
	#((y_mid - line[j,1])-slope1*x_mid +slope2*line[j,0])/(slope2-slope1)=x
	#x_int = ((y_mid_J - line[I,1])-slope1*x_mid_J +slope2*line[I,0])/(slope2-slope1);
	#y_int = y_mid_J +slope1*(x_int-x_mid);
	#d_2 = math.sqrt((x_mid_J-x_int)**2 + (y_mid_J-y_int)**2);



print d_max;
M =  np.shape(vote_data_valid)
#print max(vote_data_invalid[:][5])
vote = np.zeros((M[0],9));
print M[0]

for i in range(M[0]):
	cost = w_1*(1-(vote_data_valid[i][4]/d_max))+w_1*(1-(vote_data_valid[i][5]/d_max)) + w_2*(vote_data_valid[i][6]/maxlength)+w_2*(vote_data_valid[i][7]/maxlength);
	data = np.asarray([vote_data_valid[i][0],vote_data_valid[i][1],vote_data_valid[i][2],vote_data_valid[i][3],vote_data_valid[i][4],vote_data_valid[i][5],vote_data_valid[i][6],vote_data_valid[i][7],cost]);
	vote[i,:] = data;
perp_data_valid = np.zeros((M[0]*(M[0]-1)*(M[0]-2),16));
#print (M[0]*(M[0]-1)*(M[0]-2)
count = 0 ;
for i in range(M[0]):
	for j in range(i+1,M[0]):
		for k in range(j+1,M[0]):
			print count 
			#print vote[i,2]
			count = count + 1 ; 
			diff1 = (float(vote[i,2])*float(vote[j,2]) - float(vote[i,3])*float(vote[j,3]))**2; 
			diff2 = (float(vote[j,2])*float(vote[k,2]) - float(vote[j,3])*float(vote[k,3]))**2;
			data = np.asarray([i,j,k,vote[i,2],vote[i,3],vote[j,2],vote[j,3],vote[k,2],vote[k,3],diff1,diff2,diff1+diff2,vote[i,8],vote[j,8],vote[k,8],vote[i,8]+vote[j,8]+vote[k,8]])
			perp_data_valid[count,:] = data;

n= np.argmax(vote[:,8]);
m = np.argsort(perp_data_valid[:,11])[0];
img = cv2.imread('groundtruth/Images/0000000041.jpg')
print vote[n,0],vote[n,1]
x1 = int(line[vote[n,0],0]);
y1 = int(line[vote[n,0],1]);
x2 = int(line[vote[n,0],2]);
y2 = int(line[vote[n,0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[n,1],0]);
y1 = int(line[vote[n,1],1]);
x2 = int(line[vote[n,1],2]);
y2 = int(line[vote[n,1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new.jpg',img)
################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote[perp_data_valid[m,0],0],0]);
y1 = int(line[vote[perp_data_valid[m,0],0],1]);
x2 = int(line[vote[perp_data_valid[m,0],0],2]);
y2 = int(line[vote[perp_data_valid[m,0],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,0],1],0]);
y1 = int(line[vote[perp_data_valid[m,0],1],1]);
x2 = int(line[vote[perp_data_valid[m,0],1],2]);
y2 = int(line[vote[perp_data_valid[m,0],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp1.jpg',img)
################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote[perp_data_valid[m,1],0],0]);
y1 = int(line[vote[perp_data_valid[m,1],0],1]);
x2 = int(line[vote[perp_data_valid[m,1],0],2]);
y2 = int(line[vote[perp_data_valid[m,1],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,1],1],0]);
y1 = int(line[vote[perp_data_valid[m,1],1],1]);
x2 = int(line[vote[perp_data_valid[m,1],1],2]);
y2 = int(line[vote[perp_data_valid[m,1],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp2.jpg',img)
################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote[perp_data_valid[m,2],0],0]);
y1 = int(line[vote[perp_data_valid[m,2],0],1]);
x2 = int(line[vote[perp_data_valid[m,2],0],2]);
y2 = int(line[vote[perp_data_valid[m,2],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,2],1],0]);
y1 = int(line[vote[perp_data_valid[m,2],1],1]);
x2 = int(line[vote[perp_data_valid[m,2],1],2]);
y2 = int(line[vote[perp_data_valid[m,2],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp3.jpg',img)
################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote[perp_data_valid[m,0],0],0]);
y1 = int(line[vote[perp_data_valid[m,0],0],1]);
x2 = int(line[vote[perp_data_valid[m,0],0],2]);
y2 = int(line[vote[perp_data_valid[m,0],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,0],1],0]);
y1 = int(line[vote[perp_data_valid[m,0],1],1]);
x2 = int(line[vote[perp_data_valid[m,0],1],2]);
y2 = int(line[vote[perp_data_valid[m,0],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,1],0],0]);
y1 = int(line[vote[perp_data_valid[m,1],0],1]);
x2 = int(line[vote[perp_data_valid[m,1],0],2]);
y2 = int(line[vote[perp_data_valid[m,1],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,1],1],0]);
y1 = int(line[vote[perp_data_valid[m,1],1],1]);
x2 = int(line[vote[perp_data_valid[m,1],1],2]);
y2 = int(line[vote[perp_data_valid[m,1],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,2],0],0]);
y1 = int(line[vote[perp_data_valid[m,2],0],1]);
x2 = int(line[vote[perp_data_valid[m,2],0],2]);
y2 = int(line[vote[perp_data_valid[m,2],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote[perp_data_valid[m,2],1],0]);
y1 = int(line[vote[perp_data_valid[m,2],1],1]);
x2 = int(line[vote[perp_data_valid[m,2],1],2]);
y2 = int(line[vote[perp_data_valid[m,2],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp.jpg',img)