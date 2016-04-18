function [vp_2,vp_3] = find_vpoints(lines,vp_1,intn_pts,vote_matrix)
% The function takes the most voted vanishing point vp_1 and returns the
% perpendicular vanishing points
ind = find(intn_pts(:,5)==1);
suitable_set = ones(0.5*size(ind,1)*(size(ind,1)-1),2);
c_t = 0;
for i_t = 1:size(ind,1)
    for j_t = i_t:size(ind,1)
        i = ind(i_t); j = ind(j_t);
        % we first check if it satisfies the vanishing line criteria        
        if (vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vote_matrix))
            % WRITE CODE FROM HERE
            c_t = c_t +1;
            suitable_set(c_t,:) = [i,j]
        end
    end
end
value_set = vote(suitable_set(:,1))+vote(suitable_set(:,2));
[~,ind_s] = max(value_set);
vp_2 = suitable_set(ind_s,1);
vp_3 = suitable_set(ind_s,2);
end

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