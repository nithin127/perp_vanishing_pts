max_len = find_max_length(line)
vote =[]
for point in intersection_valid[2:3]:
	vote_iter = float(0)
	if (point[2] == float("inf")):
		pts = line[point[1]][0]
		if (pts[0]-pts[2] ==0):
			m = float("inf")
		else:
			m = (pts[1]-pts[3])/pts[0]-pts[2]
		for seg in line[9:10]:
			pts_t = seg[0]			
			if (pts[0]-pts[2] ==0):
				m_t = float("inf")
			else:
				m_t = (pts[1]-pts[3])/pts[0]-pts[2]
			length_t = np.sqrt((pts[1]-pts[3])**2+(pts[0]-pts[2])**2)
			#vote_iter = vote_iter + vote_value(m,m_t,length_t,max_len)
	else:
		v_x = point[2]
		v_y = point[3]
		for seg in line[9:10]:
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
