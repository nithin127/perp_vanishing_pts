
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
		if (x== float("inf")):
			return 0.0
		else:	
			return x



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
			m = (pts[1]-pts[3])/(pts[0]-pts[2])
		for seg in line:
			pts_t = seg[0]			
			if (pts[0]-pts[2] ==0):
				m_t = float("inf")
			else:
				m_t = (pts[1]-pts[3])/(pts[0]-pts[2])
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




