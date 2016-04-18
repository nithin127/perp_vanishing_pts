function [vote,vote_matrix] = vote_points(cross,lines)
% This function returns the vote value of all the intersection points
vote_matrix = cell(size(cross,1),1);
vote = zeros(size(cross,1),1);
sigma = 0.1;
threshold = 1;
ind = find(cross(:,5)==1);
for i_t = 1:size(ind,1)    
    i = ind(i_t);
    v_line = zeros(1,size(lines,1)); %pre-allocating for speed :P
    cnt =0;
    v_tot = 0;
    for j = 1:size(lines,1)
        if (cross(i,1)==inf)
            ang = cross(i,4);
        else
            ang = atan((cross(i,2)-0.5*(lines(j,3)+lines(j,4)))/...
            (cross(i,1)-0.5*(lines(j,1)+lines(j,2))));
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
