function [suitable_set,o,f] = find_vpoints(lines,vp_candidates,intn_pts,vote_matrix,size_im,grayIm)
% The function takes the most voted vanishing point vp_1 and returns the
% perpendicular vanishing points

vp_1 = vp_candidates(1);

ind = vp_candidates(2:end);
suitable_set = ones(0.5*size(ind,1)*(size(ind,1)-1),2);
c_t = 0;
for i_t = 1:size(ind,1)
    for j_t = i_t:size(ind,1)
        i = ind(i_t); j = ind(j_t);
        % we first check if it satisfies the vanishing line criteria        
        if (vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vote_matrix,grayIm))            
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
