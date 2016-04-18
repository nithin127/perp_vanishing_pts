function cross = find_intersection(lines)
% This function computes the intersection points of the lines segments
% detected in APPgetLargeConnectedEdges.m

%Note the syntax, each row in cross would be as follows
% [int_x, int_y, line1, line2, valid_point]

n =size(lines,1);
cross = zeros(n*(n-1)/2,5);
count = 0;
for i = 1:n
    for j = i:n
        count = count +1;
        if (lines(i,5) == lines(j,5))
            cross(count,:) = [inf,inf,i,j,1];
        else
            int_x = (lines(j,3)-lines(i,3)+tan(lines(i,5))*lines(i,1)-...
                tan(lines(j,5))*lines(j,1))/(tan(lines(i,5))-tan(lines(j,5)));
            int_y = tan(lines(i,5))*(int_x - lines(i,1))+lines(i,3);
            cross(count,:) = [int_x,int_y,i,j,1];
            if (in_line_seg(int_x,int_y,i,lines) || in_line_seg(int_x,int_y,j,lines))
                cross(count,5) = 0;
            end
        end
    end
end    
     
end

function res = in_line_seg(x,y,ind,lines)
%This function would return true if the point(int_x,int_y) lies inside the
%line segment, false otherwise
v1 = [x-lines(ind,1);y-lines(ind,3)];
v2 = [x-lines(ind,2);y-lines(ind,4)];
    if v1'*v2 < 0
        res =  1;
    else
        res =  0;
    end
end