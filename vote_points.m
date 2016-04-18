function vote = vote_points(cross,lines)
% This function returns the vote value of all the intersection points
vote = zeros(size(cross,1),1);
sigma = 0.1;
ind = find(cross(:,5)==1);
for i_t = 1:size(ind,1)
    i = ind(i_t);
    for j = 1:size(lines,1)
        if (cross(i,1)==inf)
            ang = cross(i,4);
        else
            ang = atan((cross(i,2)-0.5*(lines(j,3)+lines(j,4)))/...
            (cross(i,1)-0.5*(lines(j,1)+lines(j,2))));
        end
        ang = abs(ang - lines(j,5));
        len = sqrt((lines(j,1)-lines(j,2))^2+(lines(j,3)-lines(j,4))^2);
        v = len*exp(-ang/(2*sigma*sigma));
        vote(i) = vote(i) + v;
    end 
end
