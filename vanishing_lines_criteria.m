function res = vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vp_membership)
% This function returns true, if the points satisfy the vanishing lines
% criteria, (See Rother['02] for details). It also returns true if the
% vanishing line doesn't exist, i.e both the vanishing points are at Inf

% We define the thresholds here
a_thres = 5*pi/180;
d_thres = 30;

% disp([i,j,vp_1])
res1 = check_threshold_vlines(i,j,lines,intn_pts,a_thres,d_thres,vp_membership);
res2 = check_threshold_vlines(i,vp_1,lines,intn_pts,a_thres,d_thres,vp_membership);
res3 = check_threshold_vlines(j,vp_1,lines,intn_pts,a_thres,d_thres,vp_membership);

res = res1&&res2&&res3;


%figure(2), hold off, imshow(1/5*grayIm)
%{
if (res == true)    
    figure(2), hold on, plot(lines(intn_pts(i,3:4),[1 2])',...
    lines(intn_pts(i,3:4),[3 4])','r')
    figure(2), hold on, plot(lines(intn_pts(j,3:4),[1 2])',...
    lines(intn_pts(j,3:4),[3 4])','b')
    figure(2), hold on, plot(lines(intn_pts(vp_1,3:4),[1 2])',...
    lines(intn_pts(vp_1,3:4),[3 4])','g')
    disp([i,j,vp_1])% checking purpose
    pause
end
%}
end

