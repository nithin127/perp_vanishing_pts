function vp_lines = determine_membership(vp,lines,vote_matrix)
% This function determines all the lines that the voting for a particular
% vanishing point
vote_threshold = 1;
angle_threshold = 5*pi/180;
vp_lines = vote_matrix{vp}{2};
vp_lines = vp_lines(1,vp_lines(2,:)>vote_threshold);
% If less lines cross the threshold, then we remove the threshold barrier
if(size(vp_lines,2)<5)
    vp_lines = vote_matrix{vp}{2}(1,:);
end
% Now, let us eliminate the outliers, if any. i.e lines having very
% different slope from the others

ang = lines(vp_lines(1),5);
% we select only the elements who came within the angle threshold
vp_lines = vp_lines((abs(lines(vp_lines,5)-ang)<= angle_threshold));
end