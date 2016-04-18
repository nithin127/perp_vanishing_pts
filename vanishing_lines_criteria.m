function res = vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vote_matrix)
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

end
