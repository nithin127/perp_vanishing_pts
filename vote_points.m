function [vote,vote_matrix] = vote_points(intn_pts,lines)
% This function returns the vote value of all the intersection points
vote_matrix = cell(size(intn_pts,1),1);
vote = zeros(size(intn_pts,1),1);
sigma = 0.1;
threshold = 1;
% Let's initialize the vote and vote matrix for the invalid points
ind = find(intn_pts(:,5)==0);
for i = 1:size(ind,1)
    i_t = ind(i);
    vote_matrix{i_t} = {0,[]};
end

% Now for the valid points
ind = find(intn_pts(:,5)==1);
ind_line = find(lines(:,7)==1);
for i_t = 1:size(ind,1)    
    i = ind(i_t);
    v_line = zeros(1,size(lines,1)); %pre-allocating for speed :P
    cnt =0;
    v_tot = 0;
    for j_t = 1:size(ind_line,1)
        j = ind_line(j_t);
        if (intn_pts(i,1)==inf)
            ang = intn_pts(i,4);
        else
            ang = atan((intn_pts(i,2)-0.5*(lines(j,3)+lines(j,4)))/...
            (intn_pts(i,1)-0.5*(lines(j,1)+lines(j,2))));
        end
        % computing the absolute value of the angle difference
        ang = abs(ang - lines(j,5));
        len = sqrt((lines(j,1)-lines(j,2))^2+(lines(j,3)-lines(j,4))^2);
        v = len*exp(-ang/(2*sigma*sigma));  
        if (v>threshold)
            %only counts the votes above a given threshold
            cnt = cnt +1;            
            v_tot = v_tot + v;
            v_line(cnt) = j;            
        end
    end
    v_line = v_line(1:cnt);
    vote(i) = v_tot;
    vote_matrix{i} = {v_tot,v_line};        
end
