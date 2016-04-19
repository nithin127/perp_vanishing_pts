import numpy as np
import cv2  
import math
import sys 
from PIL import Image
from tempfile import TemporaryFile
import pdb
import os
from pylsd import lsd
fullName = 'groundtruth/Images/0000000041.jpg'
folder, imgName = os.path.split(fullName)
src = cv2.imread(fullName, cv2.IMREAD_COLOR)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
lines = lsd(gray)
print lines[0]
print np.shape(lines)
for i in xrange(lines.shape[0]):
    pt1 = (int(lines[i, 0]), int(lines[i, 1]))
    pt2 = (int(lines[i, 2]), int(lines[i, 3]))
    width = lines[i, 4]
    cv2.line(src, pt1, pt2, (0, 0, 255), int(np.ceil(width / 2)))
cv2.imwrite('check.jpg', src)
###########################333
#print np.shape(lines[0])#Check point for lines data type 
lines = lines.astype(float);
#####################The part after this is only for testing ##########333
line = lines;
l = np.shape(line);
line1  = np.zeros((l[0],5));
length = [];
#print l
maxlength  = 0 ; 
count = 0;
for i in range(l[0]):
	mod = math.sqrt((line[i,0]-line[i,2])**2 +(line[i,1]-line[i,3])**2);
	if (mod > 10):
		count = count +1;
		length.append(i);
	if (mod > maxlength):
		maxlength = mod ; 
		i_arg  = i ;
line = np.zeros((count,5));
for i in range(count):
	line[i,:] = lines[length[i],:];

#line[:,:] = line
#print max(length);
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
l = np.shape(line);
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




#print max(vote_data_invalid[:][5])

#print M[0]
#print np.asarray([-10:-1]);
N = np.shape(intersection_valid);
M = np.shape(line);
vote = np.zeros((N[0],4));
print N[0]
w_1 = 0.25;#10e5	 
w_2 = 0.75;#10e10
data_line = np.zeros((N[0],M[0]));
for i in range(N[0]):
	print i
	cost = 0 ;
	x_int = intersection_valid[i][2];
	y_int = intersection_valid[i][3];
	l = [];
	for j in range(M[0]):
		x_mid = ((line[j,0] +line[j,2])/2);
		y_mid = ((line[j,1] +line[j,3])/2);
		x_1  = line[j,0];
		y_1  = line[j,1];
		x_2  = line[j,2];
		y_2  = line[j,3];
		length1 = math.sqrt((x_1-x_2)**2 + (y_1-y_2)**2);
		length2 = math.sqrt((x_mid-x_int)**2 + (y_mid-y_int)**2);
		d_1 = math.acos(abs(((x_1-x_2)*(x_int - x_mid) + (y_1-y_2)*(y_int-y_mid))/((length1+0.0000001)*length2)));
		if (d_1 < 0.08726646259971647):
			cost = cost + w_1*(1-((d_1)/(0.08726646259971647))) + w_2*(length1/maxlength);
			data_line[i,j] = 1;
	vote[i,:] = np.asarray([d_1,length1,length2,cost]);		
#
#print max(max(vote[:,0]),max(vote[:,1]));
#print max(vote[:,4])
#t_alpha = max(max(vote[:,5]),max(vote[:,6]));
#t_alpha_min = min(min(vote[:,5]),min(vote[:,6]));
#print t_alpha
#d_max = max(max(vote[:,0]),max(vote[:,1]));
#t_alpha =(0.2*t_alpha + 0.8*t_alpha_min);
#d_max       = d_max/4;
#print d_max; 
#print t_alpha;
n= np.argsort(vote[:,3])[-1];

img = cv2.imread('groundtruth/Images/0000000041.jpg')
#print vote[n,0],vote[n,1]
x1 = int(line[intersection_valid[n][0],0]);
y1 = int(line[intersection_valid[n][0],1]);
x2 = int(line[intersection_valid[n][0],2]);
y2 = int(line[intersection_valid[n][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[n][1],0]);
y1 = int(line[intersection_valid[n][1],1]);
x2 = int(line[intersection_valid[n][1],2]);
y2 = int(line[intersection_valid[n][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new.jpg',img)
##################################
#x1 = int(line[intersection_valid[n][0],0]);
#y1 = int(line[intersection_valid[n][0],1]);
#x2 = int(intersection_valid[n][2]);
#y2 = int(intersection_valid[n][3]);
#cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#cv2.imwrite('houghlines_new.jpg',img)
##################################
m = np.argsort(-vote[:,3]);
print m[0]
a =  data_line[m[0],0] 
vote_new = vote[m,:];
vote = vote[m[:],:];
N = np.shape(vote);
M = np.shape(line); 
print M[0]
print N[0]
k_test = 0;
k_test1 = 0;
k_test2 = 0;
k_test3 = 0;
i = 0 ;
count_arg = 0 ;
#perpdata_new = np.zeros(((N[0],N[0],N[0])));
maxval = 0 ;
maxval1 = 0;
print data_line[m[1],0]
for i in range(1,2):
	#i = i +1 ;
	print i 
	x_int1 = intersection_valid[m[i-1]][2];
	y_int1 = intersection_valid[m[i-1]][3];
	j = i+1;
	for j in range(i+1,N[0]+1) :
		print j
		#j = j +1; 	
		x_int2 = intersection_valid[m[j-1]][2];
		y_int2 = intersection_valid[m[j-1]][3];
		length1 = math.sqrt((x_int1-x_int2)**2 +(y_int1-y_int2)**2);
		k = j +1 ; 
		for k in range(j+1,N[0]+1):
			#print k
			#k = k +1 ;
			x_int3 = intersection_valid[m[k-1]][2];
			y_int3 = intersection_valid[m[k-1]][3];
			length2 = math.sqrt((x_int2-x_int3)**2 +(y_int2-y_int3)**2);
			length3 = math.sqrt((x_int3-x_int1)**2 +(y_int3-y_int1)**2);
			dot1 = (x_int1 - x_int2)*(x_int3 - x_int2) + (y_int1-y_int2)*(y_int3-y_int2) ;
			#print dot1 
			if (dot1 > 0):
				dot2 = (x_int2 - x_int1)*(x_int3 - x_int1) + (y_int2-y_int1)*(y_int3-y_int1) ;
				if (dot2 > 0 ): 
					dot3 = (x_int2 - x_int3)*(x_int1 - x_int3) + (y_int2-y_int3)*(y_int1-y_int3) ;
					if(dot3 > 0 ):
						q = 0
						k_test1 = 0;
						k_test2 = 0; 
						k_test3 = 0 ;
						count1 = 0 ;
						count2 = 0 ; 
						count3 = 0;
						for q in range(1,M[0]+1):
							p= q-1;
							#q =q +1 ; 
							#print p
							if (((data_line[m[i-1],p])==1) and ((data_line[m[j-1],p])==1)):
								count1 = count1 +1 ;
								#print p;
								#print m[i],m[j],m[k]
								#print data_line[m[j],p],data_line[m[k],p]
								length1 = math.sqrt((x_int1-x_int2)**2 +(y_int1-y_int2)**2);
								x_mid = ((line[p,0]+line[p,2])/2);
								y_mid = ((line[p,1]+line[p,3])/2);
								x_1 = line[p,0];
								y_1 = line[p,1];
								x_2 = line[p,2];
								y_2  = line[p,3];
								slope = ((y_int2-y_int1)/(x_int2 - x_int1));
								dist_d = (abs((slope*(x_int1-x_mid)-(y_int1-y_mid)))/(math.sqrt(slope**2 + 1)));
								if (dist_d < 30.0):
									length2 =  math.sqrt((x_2-x_1)**2 +(y_2-y_1)**2);
									angle1 = math.acos(abs((x_int1-x_int2)*(x_1 - x_2)+(y_int1-y_int2)*(y_1 - y_2))/((length1+0.00001)*(length2+0.00001)));
									if (angle1 < 0.0872):
										k_test1 = k_test1 +1 ;
										
											
											#print k_test1
										
									 
							if (((data_line[m[j-1],p])==1) and ((data_line[m[k-1],p])==1)):
								#print p;
								count2 = count2 + 1; 
								length1 = math.sqrt((x_int2-x_int3)**2 +(y_int2-y_int3)**2);
								x_mid = ((line[p,0]+line[p,2])/2);
								y_mid = ((line[p,1]+line[p,3])/2);
								x_1 = line[p,0];
								y_1 = line[p,1];
								x_2 = line[p,2];
								y_2  =line[p,3];
								slope = ((y_int2-y_int3)/(x_int2 - x_int3));
								dist_d = (abs((slope*(x_int2-x_mid)-(y_int2-y_mid)))/(math.sqrt(slope**2 + 1)));
								if (dist_d < 30.0):
									length2 =  math.sqrt((x_1-x_2)**2 +(y_1-y_2)**2);
									angle1 = math.acos(abs((x_int2-x_int3)*(x_1 - x_2)+(y_int2-y_int3)*(y_1 - y_2))/((length1+0.00001)*(length2+0.00001)));
									if (angle1 < 0.08726646259971647):
										k_test2 = k_test2 +1 ;
							#print data_line[m[k-1],p],data_line[m[i-1],p] 		
							if (((data_line[m[k-1],p])==1) and ((data_line[m[i-1],p])==1)):
								#print p;
								count3 = count3 + 1; 
								length1 = math.sqrt((x_int3-x_int1)**2 +(y_int3-y_int1)**2);
								x_mid = ((line[p,0]+line[p,2])/2);
								y_mid = ((line[p,1]+line[p,3])/2);
								x_1 = line[p,0];
								y_1 = line[p,1];
								x_2 = line[p,2];
								y_2  =line[p,3];
								slope = ((y_int3-y_int1)/(x_int3 - x_int1));
								dist_d = (abs((slope*(x_int3-x_mid)-(y_int3-y_mid)))/(math.sqrt(slope**2 + 1)));
								if (dist_d < 30.0):
									length2 =  math.sqrt((x_2-x_1)**2 +(y_2-y_1)**2);
									angle1 = math.acos(abs((x_int3-x_int1)*(x_1 - x_2)+(y_int3-y_int1)*(y_1 - y_2))/((length1+0.0001)*(length2+0.0001)));
									if (angle1 < 0.08726646259971647):
										k_test3 = k_test3 + 1;
									
						#print ((float(k_test1)+float(k_test2)+float(k_test3))/(float(count1+0.00001)+float(count2+0.00001)+float(count3+0.00001)))
						if (k_test1 == count1 and k_test2  == count2 and k_test3 == count3 and count1 !=0 and count2 !=0 and count3 != 0):
							maxval1 = maxval1 + 1;
							#print maxval1
							countarg = vote[i-1,3] + vote[j-1,3] + vote[k-1,3]; 
							if (countarg > maxval):
								maxval = countarg	
								i_arg = i-1
						 		j_arg = j-1
								k_arg = k-1


print maxval
#i,j,k = np.unravel_index(perpdata_new.argmax(), perpdata_new.shape)
#print data_line
#print np.size(I)
#print perpdata_new
#i = I[0]+1;
#j = I[1]+1;
#k = I[2]+1;	
i = i_arg+1;
j = j_arg + 1;
k = k_arg +1 ; 

img = cv2.imread('groundtruth/Images/0000000041.jpg')
#print vote[n,0],vote[n,1]
x1 = int(line[intersection_valid[m[i-1]][0],0]);
y1 = int(line[intersection_valid[m[i-1]][0],1]);
x2 = int(line[intersection_valid[m[i-1]][0],2]);
y2 = int(line[intersection_valid[m[i-1]][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[i-1]][1],0]);
y1 = int(line[intersection_valid[m[i-1]][1],1]);
x2 = int(line[intersection_valid[m[i-1]][1],2]);
y2 = int(line[intersection_valid[m[i-1]][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[j-1]][0],0]);
y1 = int(line[intersection_valid[m[j-1]][0],1]);
x2 = int(line[intersection_valid[m[j-1]][0],2]);
y2 = int(line[intersection_valid[m[j-1]][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[j-1]][1],0]);
y1 = int(line[intersection_valid[m[j-1]][1],1]);
x2 = int(line[intersection_valid[m[j-1]][1],2]);
y2 = int(line[intersection_valid[m[j-1]][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[k-1]][0],0]);
y1 = int(line[intersection_valid[m[k-1]][0],1]);
x2 = int(line[intersection_valid[m[k-1]][0],2]);
y2 = int(line[intersection_valid[m[k-1]][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[k-1]][1],0]);
y1 = int(line[intersection_valid[m[k-1]][1],1]);
x2 = int(line[intersection_valid[m[k-1]][1],2]);
y2 = int(line[intersection_valid[m[k-1]][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#x1 = int(line[intersection_valid[m[i]][0],0]);
#y1 = int(line[intersection_valid[m[i][0],1]);
#x2 = int(intersection_valid[n][2]);
#y2 = int(intersection_valid[n][3]);
#cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp.jpg',img)
##############################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
#print vote[n,0],vote[n,1]
x1 = int(line[intersection_valid[m[i-1]][0],0]);
y1 = int(line[intersection_valid[m[i-1]][0],1]);
x2 = int(line[intersection_valid[m[i-1]][0],2]);
y2 = int(line[intersection_valid[m[i-1]][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[i-1]][1],0]);
y1 = int(line[intersection_valid[m[i-1]][1],1]);
x2 = int(line[intersection_valid[m[i-1]][1],2]);
y2 = int(line[intersection_valid[m[i-1]][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp_1.jpg',img)
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[intersection_valid[m[j-1]][0],0]);
y1 = int(line[intersection_valid[m[j-1]][0],1]);
x2 = int(line[intersection_valid[m[j-1]][0],2]);
y2 = int(line[intersection_valid[m[j-1]][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[j-1]][1],0]);
y1 = int(line[intersection_valid[m[j-1]][1],1]);
x2 = int(line[intersection_valid[m[j-1]][1],2]);
y2 = int(line[intersection_valid[m[j-1]][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp_2.jpg',img)
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[intersection_valid[m[k-1]][0],0]);
y1 = int(line[intersection_valid[m[k-1]][0],1]);
x2 = int(line[intersection_valid[m[k-1]][0],2]);
y2 = int(line[intersection_valid[m[k-1]][0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[intersection_valid[m[k-1]][1],0]);
y1 = int(line[intersection_valid[m[k-1]][1],1]);
x2 = int(line[intersection_valid[m[k-1]][1],2]);
y2 = int(line[intersection_valid[m[k-1]][1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
#x1 = int(line[intersection_valid[m[i]][0],0]);
#y1 = int(line[intersection_valid[m[i][0],1]);
#x2 = int(intersection_valid[n][2]);
#y2 = int(intersection_valid[n][3]);
#cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp_3.jpg',img)
#######################################################
print intersection_valid[m[i-1]][2];
print intersection_valid[m[i-1]][3];
print intersection_valid[m[j-1]][2];
print intersection_valid[m[j-1]][3];
print intersection_valid[m[k-1]][2];
print intersection_valid[m[k-1]][3];
print line[intersection_valid[m[i-1]][0],:]
print line[intersection_valid[m[i-1]][1],:]
print line[intersection_valid[m[j-1]][0],:]
print line[intersection_valid[m[j-1]][1],:]
print line[intersection_valid[m[k-1]][0],:]
print line[intersection_valid[m[k-1]][1],:]



'''
a =  np.argsort(vote[:,8])[0:20];
#print np.argsort(vote[:,8])[422:441];
vote_new = vote[a,:];
print vote[a[1],-1];
print np.shape(vote_new);	
M =  np.shape(vote_new);
print M[0];
#print M[0]*(M[0]-1)*(M[0]-2);
perp_data_valid = np.zeros(((M[0]*(M[0]-1)*(M[0]-2)/6),18));
count = 0 ;
m_arg = -1 ;
for i in range(M[0]):
	for j in range(i+1,M[0]):
		for k in range(j+1,M[0]):
			print count 
			#print vote[i,2]
			count = count + 1 ; 
			diff1 = (float(vote_new[i,2])*float(vote_new[j,2]) + float(vote_new[i,3])*float(vote_new[j,3])-(float(vote_new[j,2])*float(vote_new[k,2]) + float(vote_new[j,3])*float(vote_new[k,3])))**2; 
			diff2 = (float(vote_new[j,2])*float(vote_new[k,2]) + float(vote_new[j,3])*float(vote_new[k,3])-(float(vote_new[k,2])*float(vote_new[i,2]) + float(vote_new[k,3])*float(vote_new[i,3])))**2;
			#print diff1+diff2;
			if ((vote[i,0] != vote[j,0]) and (vote[i,0] != vote[j,1]) and (vote[i,1] != vote[j,0]) and (vote[i,1] != vote[j,1])):
				if ((vote[j,0] != vote[k,0]) and (vote[j,0] != vote[k,1]) and (vote[j,1] != vote[k,0]) and (vote[j,1] != vote[k,1])):
					data = np.asarray([i,j,k,vote_new[i,2],vote_new[i,3],vote_new[j,2],vote_new[j,3],vote_new[k,2],vote_new[k,3],diff1,diff2,diff1+diff2,vote[i,8],vote_new[j,8],vote_new[k,8],vote_new[i,8]+vote_new[j,8]+vote_new[k,8],(vote_new[i,8]+vote_new[j,8]+vote_new[k,8])/(diff1+diff2),count-1]);
					m_arg = count -1;
					
			else :					 
				data = np.asarray([i,j,k,vote_new[i,2],vote_new[i,3],vote_new[j,2],vote_new[j,3],vote_new[k,2],vote_new[k,3],diff1,diff2,diff1+diff2,vote[i,8],vote_new[j,8],vote_new[k,8],vote_new[i,8]+vote_new[j,8]+vote_new[k,8],(vote_new[i,8]+vote_new[j,8]+vote_new[k,8])/(diff1+diff2),0])
			perp_data_valid[count-1,:] = data;

#print (M[0]*(M[0]-1)*(M[0]-2)/6);
print d_max;
np.argsort(perp_data_valid[:,11])[0];
n = np.argsort(perp_data_valid[:,11])[0:10];
perp_data_valid = perp_data_valid[n,:]
m = np.argmax(perp_data_valid[:,15]);
print m_arg
print perp_data_valid[m,11],perp_data_valid[m,15]

################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote_new[perp_data_valid[m,0],0],0]);
y1 = int(line[vote_new[perp_data_valid[m,0],0],1]);
x2 = int(line[vote_new[perp_data_valid[m,0],0],2]);
y2 = int(line[vote_new[perp_data_valid[m,0],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,0],1],0]);
y1 = int(line[vote_new[perp_data_valid[m,0],1],1]);
x2 = int(line[vote_new[perp_data_valid[m,0],1],2]);
y2 = int(line[vote_new[perp_data_valid[m,0],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp1.jpg',img)
################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote_new[perp_data_valid[m,1],0],0]);
y1 = int(line[vote_new[perp_data_valid[m,1],0],1]);
x2 = int(line[vote_new[perp_data_valid[m,1],0],2]);
y2 = int(line[vote_new[perp_data_valid[m,1],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,1],1],0]);
y1 = int(line[vote_new[perp_data_valid[m,1],1],1]);
x2 = int(line[vote_new[perp_data_valid[m,1],1],2]);
y2 = int(line[vote_new[perp_data_valid[m,1],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp2.jpg',img)
################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote_new[perp_data_valid[m,2],0],0]);
y1 = int(line[vote_new[perp_data_valid[m,2],0],1]);
x2 = int(line[vote_new[perp_data_valid[m,2],0],2]);
y2 = int(line[vote_new[perp_data_valid[m,2],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,2],1],0]);
y1 = int(line[vote_new[perp_data_valid[m,2],1],1]);
x2 = int(line[vote_new[perp_data_valid[m,2],1],2]);
y2 = int(line[vote_new[perp_data_valid[m,2],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp3.jpg',img)
#################################################
img = cv2.imread('groundtruth/Images/0000000041.jpg')
x1 = int(line[vote_new[perp_data_valid[m,0],0],0]);
y1 = int(line[vote_new[perp_data_valid[m,0],0],1]);
x2 = int(line[vote_new[perp_data_valid[m,0],0],2]);
y2 = int(line[vote_new[perp_data_valid[m,0],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,0],1],0]);
y1 = int(line[vote_new[perp_data_valid[m,0],1],1]);
x2 = int(line[vote_new[perp_data_valid[m,0],1],2]);
y2 = int(line[vote_new[perp_data_valid[m,0],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,1],0],0]);
y1 = int(line[vote_new[perp_data_valid[m,1],0],1]);
x2 = int(line[vote_new[perp_data_valid[m,1],0],2]);
y2 = int(line[vote_new[perp_data_valid[m,1],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,1],1],0]);
y1 = int(line[vote_new[perp_data_valid[m,1],1],1]);
x2 = int(line[vote_new[perp_data_valid[m,1],1],2]);
y2 = int(line[vote_new[perp_data_valid[m,1],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,2],0],0]);
y1 = int(line[vote_new[perp_data_valid[m,2],0],1]);
x2 = int(line[vote_new[perp_data_valid[m,2],0],2]);
y2 = int(line[vote_new[perp_data_valid[m,2],0],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
x1 = int(line[vote_new[perp_data_valid[m,2],1],0]);
y1 = int(line[vote_new[perp_data_valid[m,2],1],1]);
x2 = int(line[vote_new[perp_data_valid[m,2],1],2]);
y2 = int(line[vote_new[perp_data_valid[m,2],1],3]);
cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv2.imwrite('houghlines_new_perp.jpg',img)
###############################################
'''