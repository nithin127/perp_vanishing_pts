function ang = max_ang_vlines(i,j,lines,intn_pts,vote_matrix)
ang = 0;
% If either of the points are at Inf, then the criteria is satisied, if 
% both are at Inf, then the criteria doesn't apply thus we'll return the 
%min_angle possible.
if ~(intn_pts(i,2)==inf || intn_pts(j,2)==inf)    
    ang_line = atan((intn_pts(i,2)-intn_pts(j,2))/(intn_pts(i,1)-intn_pts(j,1)));
    com_lines = intersect(vote_matrix{i}{2},vote_matrix{j}{2});
    for l = com_lines
        p = abs(ang_line - lines(l,5));
        if(p>ang)
            ang = p;
        end
    end
end
end