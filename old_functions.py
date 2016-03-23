
def find_intersections(line):
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
