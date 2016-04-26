function [suitable_set,o,f] = find_vpoints(lines,vp_candidates,intn_pts,size_im,~,vp_membership)
% The function takes the most voted vanishing point vp_1 and returns the
% perpendicular vanishing points

vp_1 = vp_candidates(1);

ind = vp_candidates;
suitable_set = ones(0.5*size(ind,1)*(size(ind,1)-1),2);
c_t = 0;
% we start the iteration from i_t = 2 (as vp_1 is already chosen)
for i_t = 2:size(ind,1)
    for j_t = i_t+1:size(ind,1)
        i = ind(i_t); j = ind(j_t);
        % we first check if it satisfies the vanishing line criteria        
        if (vanishing_lines_criteria(i_t,j_t,1,lines,intn_pts,vp_membership)) 
            % Note: vanishing line criteria would always be satisfied as
            % there are no common intersection lines. 
            % We are giving i_t,j_t into vanishing_lines criteria and  i,j
            % into orthogonality criteria 
            [res,o,f] = orthogonality_criteria(i,j,vp_1,intn_pts,size_im,lines);
            if (res)
                c_t = c_t +1;
                suitable_set(c_t,:) = [i,j];
                disp([i,j])
            end
        end
    end
end
suitable_set = suitable_set(1:c_t,:);
end
