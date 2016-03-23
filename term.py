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


'''
cv2.circle(img1,(int(p_x),int(p_y)),3,(255,0,0),-1)
'''


