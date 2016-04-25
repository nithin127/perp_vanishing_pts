
suitable_set = [vp_candidates(2),vp_candidates(4)];
vp_1 = vp_candidates(1);
i = vp_candidates(2);
j = vp_candidates(4);
%vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vote_matrix,grayIm)

a_thres = 5*pi/180;
d_thres = 30;

% disp([i,j,vp_1])
res1 = check_threshold_vlines(1,2,lines,intn_pts,vote_matrix_init,a_thres,d_thres);
res2 = check_threshold_vlines(2,4,lines,intn_pts,vote_matrix_init,a_thres,d_thres);
res3 = check_threshold_vlines(1,4,lines,intn_pts,vote_matrix_init,a_thres,d_thres);

res = res1&&res2&&res3;

