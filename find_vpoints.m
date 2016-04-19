function [vp_2,vp_3,o,f] = find_vpoints(lines,vp_1,intn_pts,vote_matrix,size_im)
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
            [res,o,f] = orthogonality_criteria(i,j,vp_1,intn_pts,size_im,lines);
            if (res)
                c_t = c_t +1;
                suitable_set(c_t,:) = [i,j];
                [i,j]
            end
        end
    end
end
suitable_set = suitable_set(1:c_t,:);
value_set = vote(suitable_set(:,1))+vote(suitable_set(:,2));
[~,ind_s] = max(value_set);
vp_2 = suitable_set(ind_s,1);
vp_3 = suitable_set(ind_s,2);
end
