function res = vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vote_matrix,grayIm)
% This function returns true, if the points satisfy the vanishing lines
% criteria, (See Rother['02] for details). It also returns true if the
% vanishing line doesn't exist, i.e both the vanishing points are at Inf

% We define the angle threshold here
ang_thres = pi/8;
res = true;

ang = max_ang_vlines(i,j,lines,intn_pts,vote_matrix);
if (ang > ang_thres) 
    res = false; 
end

ang = max_ang_vlines(i,vp_1,lines,intn_pts,vote_matrix);
if (ang > ang_thres) 
    res = false; 
end

ang = max_ang_vlines(j,vp_1,lines,intn_pts,vote_matrix);
if (ang > ang_thres) 
    res = false; 
end
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
