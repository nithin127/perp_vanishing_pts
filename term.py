zero_slope = []
inf_slope=[]
other_line=[]
image_dir = 'groundtruth/Images/0000000041.jpg'

for i in range(line.shape[0]):
	if (line[i][0][3]-line[i][0][1] == 0):	
		zero_slope.append((line[i],i))
		cv2.line(img,(int(line[i][0][0]),int(line[i][0][1])),(int(line[i][0][2]),int(line[i][0][3])),(255,0,0),2)

for i in range(line.shape[0]):
	if (line[i][0][2]-line[i][0][0] == 0):		
		inf_slope.append((line[i],i))
		cv2.line(img,(int(line[i][0][0]),int(line[i][0][1])),(int(line[i][0][2]),int(line[i][0][3])),(0,0,255),2)

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

'''img1 = cv2.imread(image_dir)
				cv2.circle(img1,(int(p_x),int(p_y)),3,(255,0,0),-1)
				cv2.line(img1,(int(other_line[i][0][0][0]),int(other_line[i][0][0][1])),(int(other_line[i][0][0][2]),int(other_line[i][0][0][3])),(0,255,0),2)
				cv2.line(img1,(int(other_line[j][0][0][0]),int(other_line[j][0][0][1])),(int(other_line[j][0][0][2]),int(other_line[j][0][0][3])),(0,0,255),2)
				mj = (other_line[j][0][0][3]-other_line[j][0][0][1])/(other_line[j][0][0][2]-other_line[j][0][0][0])
				mi = (other_line[i][0][0][3]-other_line[i][0][0][1])/(other_line[i][0][0][2]-other_line[i][0][0][0])
				for g in np.linspace(0,666,50):
					yi = other_line[i][0][0][1]+(mi)*(g-other_line[i][0][0][0])
					yj = other_line[j][0][0][1]+(mj)*(g-other_line[j][0][0][0])					
					cv2.circle(img1,(int(g),int(yi)),1,(0,255,0),-1)
					cv2.circle(img1,(int(g),int(yj)),1,(0,255,0),-1)
				cv2.imwrite('invalid_'+str(i)+'_'+str(j)+'_'+image_dir[-6:],img1)'''				